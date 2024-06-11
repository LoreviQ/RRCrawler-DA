"""
This module contains classes for the Royal Road crawler.

Author: Oliver Jay
Version: 1.0
License: MIT
"""

import enum
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from data import DataHandler

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)


class PageType(enum.Enum):
    """Enum for the type of page being crawled."""

    SEARCH = "search"
    FICTION = "fiction"
    CHAPTER = "chapter"


class URL:
    """Class to represent a URL to be crawled."""

    def __init__(self, url, page_type):
        self.url = url
        self.page_type = page_type

    def __eq__(self, other):
        return self.url == other.url


class RRCrawler:
    """Class to crawl Royal Road."""

    def __init__(self, urls, data_handler=DataHandler()):
        """Initializes the crawler with a list of URLs to visit."""
        self.urls_to_visit = urls
        self.urls_visited = []
        self.data_handler = data_handler

    def download(self, url):
        """Downloads the HTML of the given URL."""
        logging.info("Downloading: %s", url.url)
        response = requests.get(url.url, timeout=5)
        if response.status_code == 200:
            return response.text
        logging.error("Failed to download %s", url.url)
        return None

    def get_new_urls(self, url, html):
        """Parses the HTML and returns the URLs of interest."""
        soup = BeautifulSoup(html, "html.parser")
        match url.page_type:
            case PageType.SEARCH:
                # yield the urls of all elements named "fiction-title" in the html
                for fiction in soup.find_all(class_="fiction-title"):
                    yield self.extract_search_data(fiction, url)
                    break  # remove to run across whole site
            case PageType.FICTION:
                fiction_id = int(url.url.split("/")[4])
                header = soup.find("div", class_="row fic-header")
                author = header.find("a").text
                fiction = self.data_handler.get_fiction(fiction_id)
                if fiction:
                    self.data_handler.update_fiction(
                        fiction_id,
                        fiction[1:-1] + [author],
                    )
                else:
                    self.data_handler.new_fiction([fiction_id] + [None] * 7 + [author])
                chapter = soup.find("tr", class_="chapter-row")
                if chapter:
                    yield URL(
                        urljoin(url.url, chapter.find("a")["href"]), PageType.CHAPTER
                    )

            case PageType.CHAPTER:
                logging.info("Chapter not yet implemented")
            case _:
                logging.error("Unknown page type: %s", url.page_type)

    def add_new_urls(self, url):
        """Adds the given URL to the list of URLs to visit."""
        if url not in self.urls_to_visit and url not in self.urls_visited:
            self.urls_to_visit.append(url)

    def crawl(self, target_url):
        """Crawls the given URL."""
        html = self.download(target_url)
        if html:
            for url in self.get_new_urls(target_url, html):
                if url:
                    logging.info(
                        "Found: %s, type %s",
                        url.url,
                        url.page_type,
                    )
                    self.add_new_urls(url)

    def run(self, N):
        """Runs the crawler."""
        url = self.urls_to_visit.pop(0)
        for i in range(N):
            self.add_new_urls(URL(url.url + f"?page={i+1}", PageType.SEARCH))
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info("Crawling:%s", url.url)
            try:
                self.crawl(url)
            except Exception:
                logging.exception("Failed to crawl: %s", url.url)
        self.data_handler.save()

    def extract_search_data(self, fiction, url):
        link = fiction.find("a")
        if "href" in link.attrs:
            new_url = URL(urljoin(url.url, link["href"]), PageType.FICTION)
        fiction_list = []
        fiction_list += [int(link["href"].split("/")[2])]
        fiction_list += [link.text]
        siblings = fiction.findNextSiblings()
        stats = siblings[1].contents
        i = 0
        for stat_txt in stats:
            stat_str = str.strip(stat_txt.text)
            if stat_str:
                fiction_list += [
                    int(stat_str.split(" ", maxsplit=1)[0].replace(",", ""))
                ]
                i += 1
            if i == 4:
                break
        fiction_list += [float(siblings[1].contents[3].find("span")["title"])]
        fiction_list += [[x for x in siblings[0].text.split("\n") if x != ""]]
        fiction_list += [None]
        self.data_handler.new_fiction(fiction_list)
        return new_url


if __name__ == "__main__":
    data_handler = DataHandler()
    data_handler.log()
