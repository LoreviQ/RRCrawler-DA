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
        self.filenames = {"fictions": "fictions.pkl", "chapters": "chapters.pkl"}
        if load:
            self.load()
        else:
            self.fictions = []
            self.chapters = []

    def new_fiction(self, fiction):
        """
        Adds a new fiction to the dataset.

        fiction is an 9 item list with the following format:
        [ID, title, followers, rating, views, chapters, pages, tags, author]
        and data types:
        ID: int
        title: str
        followers: int
        rating: float
        views: int
        chapters: int
        pages: int
        tags: list of str
        author: str
        """
        if len(fiction) != 9:
            raise ValueError("Fiction must have 9 items.")
        self.fictions += [fiction]

    def update_fiction(self, fiction_id, fiction):
        """
        Updates a fiction in the dataset.

        fiction_id is the ID of the fiction to update.
        fiction is an 8 item list containing the updated information.
        """
        if len(fiction) != 8:
            raise ValueError("Fiction must have 8 items.")
        for i, f in enumerate(self.fictions):
            if f[0] == fiction_id:
                self.fictions[i] = [fiction_id] + fiction
                break

    def new_chapter(self, chapter):
        """
        Adds a new chapter to the dataset.

        chapter is an 7 item list with the following format:
        [ID, fiction_id, title, date, words, chapter_number, comments]
        and data types:
        ID: int
        fiction_id: int
        title: str
        date: str
        words: int
        chapter_number: int
        comments: int
        """
        if len(chapter) != 7:
            raise ValueError("Chapter must have 7 items.")
        self.chapters += [chapter]

    def update_chapter(self, chapter_id, chapter):
        """
        Updates a chapter in the dataset.

        chapter_id is the ID of the chapter to update.
        chapter is an 6 item list containing the updated information.
        """
        if len(chapter) != 6:
            raise ValueError("Chapter must have 6 items.")
        for i, c in enumerate(self.chapters):
            if c[0] == chapter_id:
                self.chapters[i] = [chapter_id] + chapter
                break

    def save(self):
        """Saves the data to a file using pickle."""
        for attr, filename in self.filenames.items():
            with open(filename, "wb") as f:
                pickle.dump(getattr(self, attr), f)

    def load(self):
        """Loads the data from a file using pickle."""
        for attr, filename in self.filenames.items():
            try:
                with open(filename, "rb") as f:
                    setattr(self, attr, pickle.load(f))
            except FileNotFoundError:
                setattr(self, attr, [])


if __name__ == "__main__":
    # Test the DataHandler class
    data_handler = DataHandler(load=False)

    print("Testing New Fiction Method...")
    data_handler.new_fiction(
        [
            1,
            "Test Fiction",
            100,
            4.5,
            1000,
            10,
            100,
            ["fantasy", "adventure"],
            "Test Author",
        ]
    )
    data_handler.new_fiction(
        [
            2,
            "Test Fiction 2",
            200,
            4,
            3000,
            20,
            300,
            ["litrpg", "isekai"],
            "Test Author 2",
        ]
    )
    assert data_handler.fictions == [
        [
            1,
            "Test Fiction",
            100,
            4.5,
            1000,
            10,
            100,
            ["fantasy", "adventure"],
            "Test Author",
        ],
        [
            2,
            "Test Fiction 2",
            200,
            4,
            3000,
            20,
            300,
            ["litrpg", "isekai"],
            "Test Author 2",
        ],
    ]
    print("New Fiction Method test passed.")

    print("Testing New Chapter Method...")
    data_handler.new_chapter([1, 1, "Test Chapter", "2021-01-01", 1000, 1, 10])
    data_handler.new_chapter([2, 1, "Test Chapter 2", "2021-01-02", 2000, 2, 20])
    assert data_handler.chapters == [
        [1, 1, "Test Chapter", "2021-01-01", 1000, 1, 10],
        [2, 1, "Test Chapter 2", "2021-01-02", 2000, 2, 20],
    ]
    print("New Chapter Method test passed.")

    print("Testing Save Method...")
    data_handler.save()
    data_handler2 = DataHandler()
    assert data_handler2.fictions == data_handler.fictions
    print("Save Method test passed.")
