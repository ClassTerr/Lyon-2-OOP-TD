import urllib
import urllib.parse
from datetime import datetime
from typing import List
import xmltodict as x2d

from Crawlers.Crawler import Crawler
from Entities.ArxivDocument import ArxivDocument
from Entities.Document import Document


class ArxivCrawler(Crawler):

    def get_documents_by_topic(self, topic_name: str, limit: int = 100) -> List[Document]:

        urlencoded_topic = urllib.parse.quote_plus(topic_name)
        url = f'http://export.arxiv.org/api/query?search_query={urlencoded_topic}&max_results={limit}'
        xml = urllib.request.urlopen(url).read()
        data = x2d.parse(xml, force_list=['author'])

        xml_docs = data['feed']['entry']

        posts = []
        for doc in xml_docs:
            authors = [x['name'] for x in doc['author']]
            url = doc['link'][0]['@href']
            date = datetime.strptime(doc['published'], "%Y-%m-%dT%H:%M:%SZ")

            posts.append(ArxivDocument(doc['id'], doc['title'], authors, doc['summary'], url, date))

        return posts
