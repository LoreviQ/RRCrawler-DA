"""
This module contains classes for holding the data in memory and saving it with pickle

Author: Oliver Jay
Version: 1.0
License: MIT
"""


class DataHandler:
    """Class to handle the data from the Royal Road crawler."""

    def __init__(self, fictions):
        """Initializes the data handler with initial dataset"""
        if fictions:
            self.fictions = fictions
        else:
            self.fictions = []

    def new_fiction(self, fiction):
        """
        Adds a new fiction to the dataset.

        fiction is an 8 item list with the following format:
        [ID, title, followers, rating, views, chapters, pages, tags]
        and data types:
        ID: int
        title: str
        followers: int
        rating: float
        views: int
        chapters: int
        pages: int
        tags: list of str
        """
        self.fictions += [fiction]
