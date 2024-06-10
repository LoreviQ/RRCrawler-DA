import enum
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class PageType(enum.Enum):
    SEARCH = "search"
    FICTION = "fiction"
    CHAPTER = "chapter"


class URL:
    def __init__(self, url, page_type):
        self.url = url
        self.page_type = page_type
        self.visited = False


class RRCrawler:
    def __init__(self, urls=[]):
        self.urls = urls


if __name__ == "__main__":
    RRCrawler(
        [URL("https://www.royalroad.com/fictions/search?page=1", PageType.SEARCH)]
    ).run()
