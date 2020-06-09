from datetime import datetime
from typing import List, Tuple

from Entities.Document import Document
from Helpers import Helpers


class RedditDocument(Document):

    def __init__(self, id: str, title: str, author: str, text: str, url: str = None, date: datetime = datetime.now(),
                 comments: List[str] = None):
        super().__init__("reddit:" + id, title, [author], text, url, date)
        self.comments = [Helpers.cleanup_str(x) for x in comments]
        self._all_text += '. '.join(comments)
        self._type = "RedditDocument"

    def __str__(self):
        return f"RedditDocument {self._id}: {Helpers.truncate_str(self._title)}"

    def search(self, search_for: str, context_len: int = 32) -> List[Tuple[str, str, str]]:
        list = super().search(search_for, context_len)
        # for avoiding merging contexts we have to search for text separately in each part of document
        for comment in self.comments:
            list += Helpers.find_text_in_context(comment, search_for, context_len)

        return list
