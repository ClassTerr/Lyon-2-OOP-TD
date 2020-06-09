import os
from typing import Dict, List, cast

from Entities.Author import Author
from Repositories.Repository import Repository


class AuthorRepository(Repository):

    def __init__(self, data_path: str = ""):
        super().__init__(filename=os.path.join(data_path, "Authors"))
        self._data: Dict[str, Author]

    def get(self, id: str) -> Author:
        return cast(Author, super().get(id))

    def get_all(self) -> List[Author]:
        return cast(List[Author], super().get_all())
