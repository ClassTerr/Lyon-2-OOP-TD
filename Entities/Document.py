import itertools
from datetime import datetime
from typing import List, Tuple, Dict

from gensim.summarization.summarizer import summarize

from Helpers import Helpers
from NlpProcessor import NlpProcessor


class Document(object):
    text: str
    title: str
    authors: List[str]
    date: datetime

    def __init__(self, id: str, title: str, authors: List[str], text: str, url: str = None,
                 date: datetime = datetime.now()):

        if title is None or text is None:
            raise ValueError("title or text was not provided")

        self._type = "Document"
        self.id = id
        self.title: str = title
        self.authors: List[str] = authors
        self.date: datetime = date
        self.url: str = url
        self.text: str = text
        self.all_text = self.title + '. ' + self.text
        self.__sentences: List[str] or None = None
        self.__words: List[str] or None = None
        self._freq: Dict[str, int] = dict()
        self.__calculate_word_frequency()

    def __str__(self):
        return f"{self._type} {self.id}: {Helpers.truncate_str(self.title)}"

    def __repr__(self):
        return f"{self._type} {Helpers.truncate_str(self.title)}"

    def get_word_frequency(self, word: str):
        return self._freq.get(word) or 0

    def __calculate_word_frequency(self):
        words = self.get_words()
        freq = dict()
        for word in words:
            cnt = freq.get(word)
            if cnt is None:
                freq[word] = 1
            else:
                freq[word] += 1

        # sorting
        self._freq = {k: v for k, v in sorted(freq.items(), key=lambda item: item[1], reverse=True)}

    def __lt__(self, other):
        """Comparer used to sort instances of class"""
        date1 = self.date.date()
        date2 = other.date.date()

        if date1 == date2:
            return self.title < other.title
        return date1 < date2

    def get_sentences(self):
        if self.__sentences is None:
            self.__sentences = Helpers.remove_empty_list_items(NlpProcessor.get_sentences(self.all_text))

        return self.__sentences

    def summarize(self):
        return summarize(self.all_text)

    def get_top_n_words(self, n: int):
        return itertools.islice(self._freq.keys(), n)

    def search(self, search_for: str, context_len: int = 32) -> List[Tuple[str, str, str]]:
        # for avoiding merging contexts we have to search for text separately in each part of document
        list = Helpers.find_text_in_context(self.title, search_for, context_len)
        list += Helpers.find_text_in_context(self.text, search_for, context_len)
        return list

    def get_sentences_count(self):
        return len(self.get_sentences())

    def get_words(self):
        if self.__words is None:
            self.__words = NlpProcessor.preprocess(self.all_text)

        return self.__words

    def get_words_count(self):
        return len(self.get_words())

    def is_valid(self):
        if self.all_text is None or len(self.all_text) < 100 or self.id is None or self.url is None:
            return False

        return True

    def get_type(self):
        return self._type
