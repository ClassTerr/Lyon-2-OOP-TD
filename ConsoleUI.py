import os
import re
from typing import List, Dict, cast, Tuple

from pandas import DataFrame

import PrintHelper
from Crawlers.UltimateDataCrawler import UltimateDataCrawler
from DocumentInvalidException import DocumentInvalidException
from DuplicateInvalidException import DuplicateInvalidException
from Entities.Corpus import Corpus
from Entities.Document import Document
from Helpers import Helpers


class ConsoleUI:
    def __init__(self):
        self.__init_commands()
        self.__exit_requested = False

        self.__std_topics = ["Artificial Intelligence", "Blockchain", "Augmented Reality", "Virtual Reality",
                             "Cloud Computing", "Angular", "React", "DevOps", "IoT", "Big Data", "Machine Learning"]

        self.corpuses: Dict[str, Corpus] = cast(Dict[str, Corpus], dict())
        self.__crawler = UltimateDataCrawler()

        dirname = os.path.dirname(__file__)
        self.__data_path = os.path.join(dirname, "Data")
        self.__topic_crawl_count = 10
        self.__preview_size = 5
        self.__concorde_context_length = 32

        self.load_corpuses()

        pass

    def load_corpuses(self):
        print("Loading corpuses...")

        if not os.path.exists(self.__data_path):
            os.makedirs(self.__data_path)

        existed_corpuses = list(next(os.walk(self.__data_path))[1])

        for c_name in existed_corpuses:
            self.corpuses[c_name.lower()] = Corpus(c_name, self.__data_path)

    def __init_commands(self):
        self.commands = {
            "help": (self.help, ["[command]"], "Get help about commands"),
            "exit": (self.exit, [], "Exit the application"),
            "ls": (self.ls, [], "Lists all available corpora"),
            "crawl": (self.crawl, ["topic-name"],
                      "Download data from internet related to specified corpus"),
            "crawl-std": (self.crawl_std, [],
                          "Download default corpora set from internet. Useful for quick start"),
            "preview": (self.preview, ["corpus"],
                        "Show brief information about all corpora or single corpus if name specified"),
            "search": (self.search, ["text"], "Show documents containing specified text"),
            "concorde": (self.concorde, ["text", "[context-length]"], "Search text and show context"),
            "freq": (self.word_frequency, ["corpus"], "Calculates key word frequency in specified corpus"),
            "summarize": (self.summarize, ["corpus"], "Get summary about documents"),
        }

    def help(self, args):
        if len(args) > 1:
            self.__wrong_arguments("help")
            return

        # show info about command usage
        if args:
            command_name = args[0]
            command = self.commands.get(command_name)

            if command is None:
                PrintHelper.print_fail(f"Command not found: {command_name}.")
            _, args_spec, description = command
            print(description)
            print(f"Usage: {command_name} {' '.join(args_spec)}")
        else:
            PrintHelper.print_ok("Available commands:")
            for command_name in sorted(self.commands.keys()):
                _, args_spec, description = self.commands.get(command_name)
                print(f"{command_name} {' '.join(args_spec)}")

    def exit(self):
        self.__exit_requested = True

    def ls(self):
        if not self.corpuses:
            PrintHelper.print_warn("No corpuses available. Please, run crawl or crawl-std commands")
            return

        PrintHelper.print_ok("Available corpuses: ")
        for c in self.corpuses.values():
            print(c.name)

    def crawl(self, args: List[str]):
        if not args:
            self.__wrong_arguments("search")
            return

        topic_name = ' '.join(args)

        PrintHelper.print_ok(f"Crawling {topic_name}...")
        docs = self.__crawler.get_documents_by_topic(topic_name, self.__topic_crawl_count)

        topic_name_low = topic_name.lower()
        corpus = self.corpuses.get(topic_name_low)
        if corpus is None:
            corpus = Corpus(topic_name, self.__data_path)
            self.corpuses[topic_name_low] = corpus

        for doc in docs:
            try:
                corpus.add_document(doc)
            except DocumentInvalidException:
                print("Document is invalid: " + str(doc))
            except DuplicateInvalidException:
                print("Document is already loaded: " + str(doc))
            pass

        corpus.save()

    def crawl_std(self):
        for t in self.__std_topics:
            self.crawl([t])
        pass

    def search(self, args: List[str]):
        if not args:
            self.__wrong_arguments("search")
            return

        text = ' '.join(args)

        res = []

        for c in self.corpuses.values():
            res += c.search(text)

        if not res:
            print("Nothing was found")
            return

        df = DataFrame([[x.get_date(), Helpers.truncate_str(x.get_title())] for x in set(res)],
                       columns=['Date', 'Document title'])
        df.index += 1

        print(df)

    def concorde(self, args: List[str]):
        if not args:
            self.__wrong_arguments("concorde")
            return

        text = ' '.join(args)

        res: List[Tuple[Document, Tuple[str, str, str]]] = []

        for c in self.corpuses.values():
            res += c.concorde(text, self.__concorde_context_length)

        if not res:
            print("Nothing was found")
            return

        data = []

        for doc, (left, mid, right) in res:
            data.append([Helpers.truncate_str(doc.get_title()), left, mid, right])

        df = DataFrame(data, columns=['Document title', 'Left context', "Text", "Right context"])

        df.index += 1
        print(df)

    def word_frequency(self, args: List[str]):
        if not args:
            self.__wrong_arguments("search")
            return

        corpus_name = ' '.join(args)
        corpus = self.corpuses.get(corpus_name)
        if corpus is None:
            self.__wrong_usage("preview", f"corpus {corpus_name} not found")
            return

        df = corpus.get_word_statistics()

        print(df)

    def summarize(self, args: List[str]):
        if not args:
            self.__wrong_arguments("summarize")
            return

        corpus_name = ' '.join(args)
        corpus = self.corpuses.get(corpus_name)
        if corpus is None:
            self.__wrong_usage("summarize", f"corpus {corpus_name} not found")
            return

        for d in corpus.get_documents():
            print(f"{d}")
            print(d.summarize())
            print('\n')
            print("Top 10 words:\n" + '\n'.join([str(x) for x in d.get_top_n_words(10)]))
            print('\n')

    def preview(self, args: List[str]):
        if not args:
            self.__wrong_arguments("search")
            return

        topic_name = ' '.join(args)

        if topic_name is None:
            for c in self.corpuses.values():
                self.preview([c.name])

        else:
            topic_name_low = topic_name.lower()
            corpus = self.corpuses.get(topic_name_low)
            if corpus is None:
                self.__wrong_usage("preview", f"corpus {topic_name} not found")
                return

            print(corpus.preview())
        pass

    def start(self):
        print("Université Lumière Lyon 2")
        print("Advanced programming cours")
        print("Author Artem Balianytsia")

        self.__exit_requested = False
        while not self.__exit_requested:
            inp = input("Enter command: ")
            command, args = ConsoleUI.__read_command(inp)
            self.execute(command, args)

    def execute(self, command_name, args):
        command = self.commands.get(command_name)

        if command is None:
            PrintHelper.print_fail(f"Command not found: {command_name}.\n"
                                   f"Use help to learn available commands")
            return

        handler, args_spec, description = command

        if args_spec:
            handler(args)
        else:
            handler()

    @staticmethod
    def __read_command(inp):
        parsed_command = [x.lower().strip('"') for x in re.split(r"\s+", inp)]
        command: str = parsed_command[0]
        args: List[str] = parsed_command[1:]
        return command, args

    def __wrong_arguments(self, command: str):
        self.__wrong_usage(command, "Wrong arguments count passed.")

    def __wrong_usage(self, command: str, message: str = ""):
        PrintHelper.print_fail(f"Wrong {command} command usage. {message}")
        self.execute("help", [command])
