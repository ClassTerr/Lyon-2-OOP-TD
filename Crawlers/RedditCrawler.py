from datetime import datetime
from typing import List

import praw

from Crawlers.Crawler import Crawler
from Entities.Document import Document
from Entities.RedditDocument import RedditDocument


class RedditCrawler(Crawler):
    def __init__(self):
        self.__redditClient = praw.Reddit(client_id='rekM6m5JkPg4Qw',
                                          client_secret='CxLWiPvFVwpOa7JYPHq4f-Lox94',
                                          user_agent='test')

    def get_documents_by_topic(self, topic_name: str, limit: int = 100) -> List[Document]:
        hot_posts = self.__redditClient.subreddit("all").search(topic_name, limit=limit)

        posts = []
        for post in hot_posts:
            post.comments.replace_more(limit=0)
            comments = [c.body for c in post.comments if c.body != '[deleted]' and c.body != '[removed]']
            posts.append(RedditDocument(post.id, post.title, post.author.name, post.selftext, post.url,
                                        datetime.fromtimestamp(post.created), comments))

        return posts
