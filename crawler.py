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

    def __eq__(self, other):
        return self.url == other.url


class RRCrawler:
    def __init__(self, urls=[]):
        self.urls_to_visit = urls
        self.urls_visited = []

    def download(self, url):
        logging.info(f"Downloading: {url.url}")
        response = requests.get(url.url)
        if response.status_code == 200:
            return response.text
        logging.error(f"Failed to download {url.url}")
        return None

    def get_new_urls(self, url, html):
        soup = BeautifulSoup(html, "html.parser")
        match url.page_type:
            case PageType.SEARCH:
                # yield the urls of all elements named "fiction-title" in the html
                for link in soup.find_all("a"):
                    logging.info(f"Found: {link["href"]}")
                    yield URL(urljoin(url.url, link["href"]), PageType.FICTION)

    def add_new_urls(self, url):
        if url not in self.urls_to_visit and url not in self.urls_visited:
            self.urls_to_visit.append(url)

    def crawl(self, target_url):
        html = self.download(target_url)
        if html:
            for url in self.get_new_urls(target_url, html):
                logging.info(f"Found: {url.url}")
                self.add_new_urls(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f"Crawling: {url.url}")
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f"Failed to crawl: {url}")


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
