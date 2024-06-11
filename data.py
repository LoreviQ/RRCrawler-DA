"""
This module contains classes for holding the data in memory and saving it with pickle

Author: Oliver Jay
Version: 1.0
License: MIT
"""

import pickle


class DataHandler:
    """Class to handle the data from the Royal Road crawler."""

    def __init__(self, load=True):
        """Initializes the data handler with initial dataset"""
        if load:
            self.load()
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

    def save(self):
        """Saves the data to a file using pickle."""

        with open("fictions.pkl", "wb") as f:
            pickle.dump(self.fictions, f)

    def load(self):
        """Loads the data from a file using pickle."""
        try:
            with open("fictions.pkl", "rb") as f:
                self.fictions = pickle.load(f)
        except FileNotFoundError:
            self.fictions = []


if __name__ == "__main__":
    # Test the DataHandler class
    data_handler = DataHandler(load=False)
    print("Testing New Fiction Method...")
    data_handler.new_fiction(
        [1, "Test Fiction", 100, 4.5, 1000, 10, 100, ["fantasy", "adventure"]]
    )
    data_handler.new_fiction(
        [2, "Test Fiction 2", 200, 4, 3000, 20, 300, ["litrpg", "isekai"]]
    )
    assert data_handler.fictions == [
        [1, "Test Fiction", 100, 4.5, 1000, 10, 100, ["fantasy", "adventure"]],
        [2, "Test Fiction 2", 200, 4, 3000, 20, 300, ["litrpg", "isekai"]],
    ]
    print("New Fiction Method test passed.")
    print("Testing Save Method...")
    data_handler.save()
    data_handler2 = DataHandler()
    assert data_handler2.fictions == data_handler.fictions
    print("Save Method test passed.")
