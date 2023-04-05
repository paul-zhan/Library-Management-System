from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from database import Database


class BookSelect:
    
    def __init__(self):
        self.d = Database()
        self.x = 51

    def get_recommendation(self, frame, x, y):
        """
        This function display the figure of the top 3 best book
        Args:
            frame  : frame that the graph will be display on 
            x : x location for the recommandation table
            y : y location for the recommandation table

        """
        recomendation = self.d.recommendation_system(frame, x, y)
        book_name_list = []
        count_list = []
        for i in recomendation:
            book_name_list.append(i[0])
            count_list.append(i[2])

        # this is where we display the matplotlib figure 
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(book_name_list, count_list)
        ax.set_title("Top 3 borrowed books")
        ax.set_xlabel("Books")
        ax.set_ylabel("Borrow times")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=1, columnspan=2)

    def buying_books(self, title, frame, x, y):
        """
        This function will be used to buy book by inserting the title of the book.

        Args:
            title : title of the book
            frame : frame where the label is going to be displayed on
            x : x location of the label
            y : y location of the label
        """
        result = self.d.checking_book_status_by_title(title)
        print(result)
        if len(result) > 0:
            self.d.insert_data_table1(self.x, result[0][1])
            label_sucess = Label(
                frame, text="A copy of the book have been added", font=("Times", 30))
            label_sucess.grid(row=x, column=y)
            frame.after(3000, lambda: label_sucess.destroy())
            self.x = self.x + 1

        else:
            label_fail = Label(
                frame, text="the transaction is not successful", font=("Times", 30))
            label_fail.grid(row=x, column=y)
            frame.after(3000, lambda: label_fail.destroy())
