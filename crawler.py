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

    def __eq__(self, other):
        return self.url == other.url


class RRCrawler:
    def __init__(self, urls=[]):
        self.urls = urls

    def download(self, url):
        response = requests.get(url.url)
        if response.status_code == 200:
            return response.text
        logging.error(f"Failed to download {url.url}")
        return None

    def get_new_urls(self, url, html):
        soup = BeautifulSoup(html, "html.parser")
        match url.page_type:
            case PageType.SEARCH:
                # yield the urls of all elements bamed "fiction-title" in the html
                for link in soup.find_all("a", class_="fiction-title"):
                    yield URL(urljoin(url.url, link["href"]), PageType.FICTION)
            case _:
                return "invalid page type"


if __name__ == "__main__":
    if True:
        RRCrawler(
            [URL("https://www.royalroad.com/fictions/search?page=1", PageType.SEARCH)]
        ).run()
    else:
        print(
            urljoin(
                "https://www.royalroad.com/fictions/search?page=1",
                "/fiction/21220/mother-of-learning",
            )
        )
