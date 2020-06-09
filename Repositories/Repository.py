import os
import pickle
from typing import Dict, List

from DuplicateInvalidException import DuplicateInvalidException


class Object(object):
    pass


class Repository:

    def __init__(self, filename: str):
        filename, file_extension = os.path.splitext(filename)
        if file_extension is None or file_extension == '':
            filename += ".pickle"

        self.__filename = filename  # private field
        self._data: Dict[str, object] = dict()  # protected field used to be overwritten in subclasses
        self.is_loaded: bool = False  # public field

    def save(self):
        dirname = os.path.dirname(self.__filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        with open(self.__filename, 'wb') as f:
            pickle.dump(self._data, f)

    def load(self):
        try:
            with open(self.__filename, 'rb') as f:
                self._data = pickle.load(f)
            self.is_loaded = True
        except FileNotFoundError:
            self.is_loaded = True

    def ensure_loaded(self):
        if not self.is_loaded:
            self.load()

    def get(self, id: str) -> object:
        self.ensure_loaded()

        return self._data.get(id)

    def get_all(self) -> List[object]:
        self.ensure_loaded()

        return list(self._data.values())

    def add(self, id: str, value):
        self.ensure_loaded()

        if id in self._data:
            raise DuplicateInvalidException(id)

        self._data[id] = value

    def count(self):
        self.ensure_loaded()

        return len(self._data)

    def __len__(self):
        return self.count()
