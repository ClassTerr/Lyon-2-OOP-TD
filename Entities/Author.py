from typing import List, Set


class Author:
    def __init__(self, name: str):
        self.name = name
        self.__publications: Set[str] = set()

    def add_publication(self, doc_id: str):
        self.__publications.add(doc_id)

    def remove_publication(self, doc_id: str):
        self.__publications.remove(doc_id)

    def get_publications(self):
        return set(self.__publications)

    def get_publications_count(self):
        return len(self.__publications)

    def __str__(self):
        return f"Author: {self.name}, {self.get_publications_count()} publications"

    def __repr__(self):
        return str(self)
