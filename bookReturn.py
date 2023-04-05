from database import Database
from tkinter import *


class BookReturn:
    
    def __init__(self):
        self.d = Database()

    def returnBook(self, book_ID, frame, x, y):
        """_summary_

        Args:
            book_ID : book ID
             frame  : frame where all the label will be display on 
            x :  x location of the label 
            y : y location of the label
        """
        record = self.d.checking_return(book_ID)
        print(record)
        if len(record) == 0:
            label_unsuccessful = Label(
                frame, text="The transaction is not successful, try again", font=("Times", 20))
            label_unsuccessful.grid(row=x, column=y)
            # this function will delete the label on the frame after 5000 ms
            frame.after(3000, lambda: label_unsuccessful.destroy())

        else:
            self.d.update_data_database(book_ID)
            label_successful = Label(
                frame, text="The transaction is  successful", font=("Times", 20))
            label_successful.grid(row=x, column=y)
            frame.after(3000, lambda: label_successful.destroy())
