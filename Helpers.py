import re
from typing import List, Tuple


class Helpers:

    @staticmethod
    def remove_empty_list_items(lst: List):
        return list(filter(lambda x: x is not None and x != "", lst))

    @staticmethod
    def cleanup_str(string: str) -> str:
        return Helpers.remove_urls(re.sub(r'[\s]+', ' ', string).strip().lower())

    @staticmethod
    def remove_urls(string: str) -> str:
        return re.sub(r"http\S+", '', string, flags=re.MULTILINE)

    @staticmethod
    def truncate_str(string: str, max_length: int = 64) -> str:
        return (string[:max_length] + '..') if len(string) > max_length else string

    @staticmethod
    def find_text_in_context(text: str, search_for: str, context_len: int = 32) -> List[Tuple[str, str, str]]:
        search_for = re.escape(search_for)
        pattern = '(.{0,' + str(context_len) + '})(' + search_for + ')(.{0,' + str(context_len) + '})'
        return re.findall(pattern, text, flags=re.IGNORECASE)
