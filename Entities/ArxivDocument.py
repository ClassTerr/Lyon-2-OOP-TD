from Entities.Document import Document


class ArxivDocument(Document):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = "ArxivDocument"
