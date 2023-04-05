from tkinter import *
from database import Database


class Booksearch:

    def __init__(self):
        self.d = Database()

    def search(self, name_of_the_book, frame, x, y, search_by):
        """ This function is used to search item in the table.
            we can search two ways :
            the first one : by title 
            the second one : by genre

        name_of_the_book  : name fo the book we are looking for 
        frame  : frame that the graph will be display on 
        x : x location for the search table
        y : y location for the search table
        """
        if search_by == "title":
            self.d.getting_books_bytitle(name_of_the_book, frame, x, y)
        else:
            self.d.getting_books_bygenre(name_of_the_book, frame, x, y)
