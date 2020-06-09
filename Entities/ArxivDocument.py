from Entities.Document import Document
from Helpers import Helpers


class ArxivDocument(Document):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = "ArxivDocument"
