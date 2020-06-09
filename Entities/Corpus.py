import os
from typing import List, cast, Tuple

from pandas import DataFrame

from DocumentInvalidException import DocumentInvalidException
from Entities.Author import Author
from Entities.Document import Document
from Helpers import Helpers
from Repositories.AuthorRepository import AuthorRepository
from Repositories.DocumentRepository import DocumentRepository


class Corpus:
    def __init__(self, name: str, data_path: str, author_repository: AuthorRepository or None = None,
                 document_repository: DocumentRepository or None = None):
        if name is None:
            raise ValueError("Please specify name of corpus")

        self.name = name

        corpus_data_path = os.path.join(data_path, name)

        if document_repository is None:
            document_repository = DocumentRepository(corpus_data_path)
        self.__document_repository = document_repository

        if author_repository is None:
            author_repository = AuthorRepository(corpus_data_path)
        self.__author_repository = author_repository

    def get_document(self, id: str) -> Document:
        return cast(Document, self.__document_repository.get(id))

    def get_documents(self) -> List[Document]:
        return cast(List[Document], self.__document_repository.get_all())

    def get_documents_count(self):
        return self.__document_repository.count()

    def get_authors_count(self) -> int:
        return self.__author_repository.count()

    def get_authors_of_document(self, doc: Document) -> List[Author]:
        return cast(List[Author], [self.__author_repository.get(x) for x in doc.authors])

    def add_document(self, doc: Document):
        if not doc.is_valid():
            raise DocumentInvalidException(f"can't add invalid {doc} to {self}")

        self.__document_repository.add(doc.id, doc)

        for auth_name in doc.authors:
            author = self.__author_repository.get(auth_name)

            if author is None:
                author = Author(auth_name)
                author.add_publication(doc.id)
                self.__author_repository.add(auth_name, Author(auth_name))

    def preview(self, limit: int = 10) -> str:
        docs = self.__document_repository.preview(limit)

        table_str = "Nothing was found"

        if docs:
            df = DataFrame([[x.date, Helpers.truncate_str(x.title)] for x in docs], columns=['Date', 'Title'])
            df.index += 1
            table_str = str(df)

        return f'Corpus "{self.name}":\n{table_str}\n{("." * 60)}'

    def save(self):
        self.__document_repository.ensure_loaded()
        self.__document_repository.save()

        self.__author_repository.ensure_loaded()
        self.__author_repository.save()

    def concorde(self, search_for: str, context_len: int = 32) -> List[Tuple[Document, Tuple[str, str, str]]]:
        result: List[Tuple[Document, Tuple[str, str, str]]] = []
        for doc in self.__document_repository.get_all():
            res = doc.search(search_for, context_len)

            if res:
                result += [(doc, x) for x in res]

        return result

    def get_semantic_statistics(self):
        all_documents = self.get_documents()
        docs_words = [x.get_words() for x in all_documents]

        all_words_in_corpus = set([item for sublist in docs_words for item in sublist])

        freq = []

        for word in all_words_in_corpus:
            documents_with_word = 0  # count of documents that contains current word
            word_total_freq = 0  # how many times this word appeared in documents

            word_count_in_documents = []  # statistics about current row
            for doc in all_documents:
                word_freq = doc.get_word_frequency(word)
                word_count_in_documents.append(word_freq)

                if word_freq > 0:
                    documents_with_word += 1  # count if document contain this word

                word_total_freq += word_freq

            freq.append([word] + word_count_in_documents + [word_total_freq] + [documents_with_word])

        statistic_headers = ['Word frequency', 'Documents with word']
        document_headers = ["Doc " + Helpers.truncate_str(key.title, 16) for key in all_documents]
        table_columns = ['Word'] + document_headers + statistic_headers
        df = DataFrame(freq, columns=table_columns)
        df = df.sort_values(statistic_headers, ascending=[False, False]).reset_index(drop=True)
        return df

    def search(self, search_for: str, context_len: int = 32) -> List[Document]:
        return [doc for doc, _ in self.concorde(search_for, context_len)]

    def __str__(self):
        return self.preview()

    def __repr__(self):
        return f"Corpus: {self.name}: documents: {self.get_documents_count()}"
