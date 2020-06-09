from typing import List

from Crawlers.ArxivCrawler import ArxivCrawler
from Crawlers.Crawler import Crawler
from Crawlers.RedditCrawler import RedditCrawler
from Entities.Document import Document


class UltimateDataCrawler(Crawler):
    def __init__(self):
        self.__crawlers: List[Crawler] = [RedditCrawler(), ArxivCrawler()]

    def get_documents_by_topic(self, topic_name: str, limit: int = 100) -> List[Document]:
        # we need to split all elements between all crawlers
        limit_for_each = int(limit / len(self.__crawlers))
        additional_limit = limit % len(self.__crawlers)

        crawled_data = []
        for i in range(len(self.__crawlers)):
            # how many documents crawler should get
            crawl_count = limit_for_each + (1 if i < additional_limit else 0)
            crawled_data += self.__crawlers[i].get_documents_by_topic(topic_name, crawl_count)

        return crawled_data
