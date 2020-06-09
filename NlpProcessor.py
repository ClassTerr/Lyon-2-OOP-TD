# partially took from https://gist.github.com/MrEliptik/b3f16179aa2f530781ef8ca9a16499af
import re
import unicodedata
from typing import List

import contractions
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

from Helpers import Helpers


class NlpProcessor:
    nltk.download('popular', quiet=True)

    @staticmethod
    def replace_contractions(text):
        """Replace contractions in string of text"""
        return contractions.fix(text)

    @staticmethod
    def remove_URLs(sample):
        """Remove URLs from a sample string"""
        return re.sub(r"http\S+", "", sample)

    @staticmethod
    def remove_non_ascii(words: List[str]) -> List[str]:
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    @staticmethod
    def to_lowercase(words: List[str]) -> List[str]:
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    @staticmethod
    def remove_numbers(words: List[str]) -> List[str]:
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            if not re.match(r'\d', word):
                new_words.append(word)
        return new_words

    @staticmethod
    def remove_punctuation(words: List[str]) -> List[str]:
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    @staticmethod
    def remove_stopwords(words: List[str]) -> List[str]:
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words

    @staticmethod
    def stem_words(words: List[str]) -> List[str]:
        """Stem words in list of tokenized words"""
        stemmer = LancasterStemmer()
        stems = []
        for word in words:
            stem = stemmer.stem(word)
            stems.append(stem)
        return stems

    @staticmethod
    def lemmatize_verbs(words: List[str]) -> List[str]:
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for word in words:
            lemma = lemmatizer.lemmatize(word, pos='v')
            lemmas.append(lemma)
        return lemmas

    @staticmethod
    def normalize(words: List[str]) -> List[str]:
        words = NlpProcessor.remove_non_ascii(words)
        words = NlpProcessor.remove_numbers(words)
        words = NlpProcessor.to_lowercase(words)
        words = NlpProcessor.remove_punctuation(words)
        words = NlpProcessor.remove_stopwords(words)
        words = NlpProcessor.lemmatize_verbs(words)
        return words

    @staticmethod
    def word_tokenize(text: str) -> List[str]:
        # or words = nltk.word_tokenize(sample)
        sentences = NlpProcessor.get_sentences(text)
        words = [item for sublist in sentences for item in re.split(r'\s+', sublist)]
        return Helpers.remove_empty_list_items(words)

    @staticmethod
    def get_sentences(text: str) -> List[str]:
        sentences = re.split(r'[.!?]', text)
        sentences = [x.strip() for x in sentences]
        return Helpers.remove_empty_list_items(sentences)

    @staticmethod
    def preprocess(text):
        text = NlpProcessor.remove_URLs(text)
        text = NlpProcessor.replace_contractions(text)
        words = NlpProcessor.word_tokenize(text)
        # Normalize
        return NlpProcessor.normalize(words)
