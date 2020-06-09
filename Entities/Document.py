import itertools
from datetime import datetime
from typing import List, Tuple, Dict

from gensim.summarization.summarizer import summarize

from Helpers import Helpers
from NlpProcessor import NlpProcessor


class Document(object):
    _text: str
    _title: str
    _authors: List[str]
    _date: datetime

    def __init__(self, id: str, title: str, authors: List[str], text: str, url: str = None,
                 date: datetime = datetime.now()):

        if title is None or text is None:
            raise ValueError("title or text was not provided")

        self._type = "Document"
        self._id = id
        self._title: str = title
        self._authors: List[str] = authors
        self._date: datetime = date
        self._url: str = url
        self._text: str = text
        self._all_text = self._title + '. ' + self._text
        self._sentences: List[str] or None = None
        self._words: List[str] or None = None
        self._freq: Dict[str, int] = dict()
        self._calculate_word_frequency()

    def _calculate_word_frequency(self):
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

    def __str__(self):
        return f"{self._type} {self._id}: {Helpers.truncate_str(self._title)}"

    def __repr__(self):
        return f"{self._type} {Helpers.truncate_str(self._title)}"

    def get_type(self):
        return self._type

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_authors(self):
        return self._authors

    def get_date(self):
        return self._date

    def get_url(self):
        return self._url

    def get_text(self):
        return self._text

    def get_word_frequency(self, word: str):
        return self._freq.get(word) or 0

    def __lt__(self, other):
        """Comparer used to sort instances of class"""
        date1 = self.get_date().date()
        date2 = other.get_date().date()

        if date1 == date2:
            return self.get_title() < other.get_title()
        return date1 < date2

    def summarize(self):
        return summarize(self._all_text)

    def get_top_n_words(self, n: int):
        return itertools.islice(self._freq.keys(), n)

    def search(self, search_for: str, context_len: int = 32) -> List[Tuple[str, str, str]]:
        # for avoiding merging contexts we have to search for text separately in each part of document
        list = Helpers.find_text_in_context(self._title, search_for, context_len)
        list += Helpers.find_text_in_context(self._text, search_for, context_len)
        return list

    def get_sentences(self):
        if self._sentences is None:
            self._sentences = Helpers.remove_empty_list_items(NlpProcessor.get_sentences(self._all_text))

        return self._sentences

    def get_sentences_count(self):
        return len(self.get_sentences())

    def get_words(self):
        if self._words is None:
            self._words = NlpProcessor.preprocess(self._all_text)

        return self._words

    def get_words_count(self):
        return len(self.get_words())

    def get_different_words_count(self):
        return len(set(self.get_words()))

    def is_valid(self):
        if self._all_text is None or len(self._all_text) < 100 or self._id is None or self._url is None:
            return False

        return True
