"""
This module contains classes for holding the data in memory and saving it with pickle

Author: Oliver Jay
Version: 1.0
License: MIT
"""

import pickle


class DataHandler:
    """Class to handle the data from the Royal Road crawler."""

    def __init__(self, load=True, test=False):
        """Initializes the data handler with initial dataset"""
        if test:
            self.filenames = {
                "fictions": "fictions_test.pkl",
                "chapters": "chapters_test.pkl",
            }
        else:
            self.filenames = {"fictions": "fictions.pkl", "chapters": "chapters.pkl"}
        if load:
            self.load()
        else:
            self.fictions = {}
            self.chapters = {}

    def put_fiction(self, fiction):
        """
        Adds a new fiction to the dataset.

        fiction is an 9 item list with the following format:
        [ID, title, followers, rating, views, chapters, pages, tags, author]
        and data types:
        ID: int
        title: str
        followers: int
        pages: int
        views: int
        chapters: int
        rating: float
        tags: list of str
        author: str
        """
        if len(fiction) != 9:
            raise ValueError("Fiction must have 9 items.")
        self.fictions[fiction[0]] = fiction[1:]

    def get_fiction(self, fiction_id):
        """
        Returns the fiction with the given ID.

        fiction_id is the ID of the fiction to return.
        """
        if fiction_id in self.fictions:
            return self.fictions[fiction_id]
        raise ValueError("Fiction not found.")

    def put_chapter(self, chapter):
        """
        Adds a new chapter to the dataset.

        chapter is an 7 item list with the following format:
        [ID, fiction_id, title, date, words, chapter_number, comments]
        and data types:
        ID: int
        fiction_id: int
        title: str
        date: int (unixtime)
        words: int
        comments: int
        """
        if len(chapter) != 6:
            raise ValueError("Chapter must have 7 items.")
        self.chapters[chapter[0]] = chapter[1:]

    def get_chapter(self, chapter_id):
        """
        Returns the chapter with the given ID.

        chapter_id is the ID of the chapter to return.
        """
        for c in self.chapters:
            if c[0] == chapter_id:
                return c
        return None

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
                setattr(self, attr, {})

    def log(self):
        """Prints the data to the console."""
        print("Fictions:")
        for fic_id, fiction in self.fictions.items():
            print(fic_id, fiction)
        print("Chapters:")
        for chap_id, chapter in self.chapters.items():
            print(chap_id, chapter)


if __name__ == "__main__":
    # Test the DataHandler class
    data_handler = DataHandler(load=False, test=True)

    print("Testing New Fiction Method...")
    data_handler.put_fiction(
        [
            1,
            "Test Fiction",
            100,
            1000,
            10,
            100,
            4.5,
            ["fantasy", "adventure"],
            "Test Author",
        ]
    )
    data_handler.put_fiction(
        [
            2,
            "Test Fiction 2",
            200,
            3000,
            20,
            300,
            4,
            ["litrpg", "isekai"],
            "Test Author 2",
        ]
    )
    assert data_handler.fictions == {
        1: [
            "Test Fiction",
            100,
            1000,
            10,
            100,
            4.5,
            ["fantasy", "adventure"],
            "Test Author",
        ],
        2: [
            "Test Fiction 2",
            200,
            3000,
            20,
            300,
            4,
            ["litrpg", "isekai"],
            "Test Author 2",
        ],
    }
    print("New Fiction Method test passed.")

    print("Testing New Chapter Method...")
    data_handler.put_chapter([1, 1, "Test Chapter", 18916034, 1000, 10])
    data_handler.put_chapter([2, 1, "Test Chapter 2", 18916034, 2000, 20])
    assert data_handler.chapters == {
        1: [1, "Test Chapter", 18916034, 1000, 10],
        2: [1, "Test Chapter 2", 18916034, 2000, 20],
    }
    print("New Chapter Method test passed.")

    print("Testing Save Method...")
    data_handler.save()
    data_handler2 = DataHandler(load=True, test=True)
    assert data_handler2.fictions == data_handler.fictions
    print("Save Method test passed.")

    print("Testing Update Fiction Method...")
    data_handler.put_fiction(
        [
            1,
            "Updated Test Fiction",
            200,
            1500,
            15,
            150,
            4.7,
            ["fantasy", "adventure"],
            "Updated Test Author",
        ],
    )
    assert data_handler.fictions == {
        1: [
            "Updated Test Fiction",
            200,
            1500,
            15,
            150,
            4.7,
            ["fantasy", "adventure"],
            "Updated Test Author",
        ],
        2: [
            "Test Fiction 2",
            200,
            3000,
            20,
            300,
            4,
            ["litrpg", "isekai"],
            "Test Author 2",
        ],
    }
    print("Update Fiction Method test passed.")

    print("Testing Update Chapter Method...")
    data_handler.put_chapter([1, 1, "Updated Test Chapter", 18916034, 1000, 10])
    assert data_handler.chapters == {
        1: [1, "Updated Test Chapter", 18916034, 1000, 10],
        2: [1, "Test Chapter 2", 18916034, 2000, 20],
    }
    print("Update Chapter Method test passed.")
