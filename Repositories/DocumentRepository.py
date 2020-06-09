import heapq
import os
from typing import Dict, List, cast

from Entities.Document import Document
from Repositories.Repository import Repository


class DocumentRepository(Repository):

    def __init__(self, data_path: str = ""):
        super().__init__(filename=os.path.join(data_path, "Documents"))
        self._data: Dict[str, Document]

    def preview(self, limit: int = 10) -> List[Document]:
        self.ensure_loaded()
        return cast(List[Document], heapq.nlargest(limit, self._data.values()))

    def get(self, id: str) -> Document:
        return cast(Document, super().get(id))

    def get_all(self) -> List[Document]:
        return cast(List[Document], super().get_all())
