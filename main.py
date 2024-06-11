"""
Main file to run the Royal Road crawler.

Author: Oliver Jay
Version: 1.0
License: MIT
"""

from crawler import URL, PageType, RRCrawler

if __name__ == "__main__":
    RRCrawler([URL("https://www.royalroad.com/fictions/search", PageType.SEARCH)]).run(
        1
    )
