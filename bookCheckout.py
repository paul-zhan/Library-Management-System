
from tkinter import *
from database import Database


# need to review the logic

class BookCheckout:
    def __init__(self):
        self.d = Database()

    def check_memberID(self, answer, book_ID_entry, frame, x, y):
        # here it checks if the entry we get is a 4 letters or numbers
        if len(answer) == 4:
            # here we check if we get 4 digits
            correct = answer.isdigit()
            if correct:
                self.answer = answer
                # here we check if the book ID entry is empty if not we call the check book id function
                if len(book_ID_entry) != 0:
                    self.check_bookID(book_ID_entry, frame, 6, 1)
                else:
                    # display a label to let the user know what is wrong
                    label = Label(
                        frame, text="Please insert a book ID number", bg="red")
                    label.grid(row=x+4, column=y)
                    frame.after(3000, lambda: label.destroy())
            else:
                # display a label to let the user know what is wrong
                label = Label(
                    frame, text="Please insert a correct member ID", bg="red")
                label.grid(row=x+4, column=y)
                frame.after(3000, lambda: label.destroy())
        else:
            # display a label to let the user know what is wrong
            label = Label(
                frame, text="Please insert a correct member ID", bg="red")
            label.grid(row=x+2, column=y)
            frame.after(3000, lambda: label.destroy())

    def check_bookID(self, book_ID, frame, x, y):
        """Here we are looking for the book state.
        the checking tuple will give the record list of the book. based on the record, we will know what state the book is in.
        Here we have three different types of state: free , reserved and not available
         - free will allow you to checkout the book straight away 
         - reserve will only allow the person who reserve the book to checkout
         - not available will allow the user to reserve the book if the book is already reserved it will not be possible to reserve it. 

        """
        checking_tuple = self.d.checking_book_status(book_ID)

        if len(checking_tuple) == 0:
            available = "free"
        elif checking_tuple[-1][1] is not None and checking_tuple[-1][2] is None and checking_tuple[-1][3] is None:
            available = "reserved"

        elif checking_tuple[-1][1] is not None and checking_tuple[-1][2] is not None and checking_tuple[-1][3] is not None and checking_tuple[-1][4] is not None:
            available = "free"
        elif checking_tuple[-1][1] == None and checking_tuple[-1][2] is not None and checking_tuple[-1][3] is not None and checking_tuple[-1][4] is not None:
            available = "free"
        else:
            available = "not available"

        if available == "free":
            self.d.insert_data_database(
                book_ID, None, self.d.current_time, None, self.answer)
            label = Label(frame, text="The transaction is successful")
            label.grid(row=x, column=y)
            frame.after(5000, lambda: label.destroy())

        elif available == "reserved":
            if int(checking_tuple[-1][4]) == int(self.answer) and checking_tuple[-2][3] is not None:
                self.d.update_data_checkout(book_ID)
                label = Label(
                    frame, text="The transaction is successful", font=("Times", 20))
                label.grid(row=x, column=y)
                frame.after(5000, lambda: label.destroy())
            else:
                label = Label(
                    frame, text="The transaction is not successful, try again ", font=("Times", 20))
                label.grid(row=x, column=y)
                frame.after(1000, lambda: label.destroy())

        else:
            label = Label(
                frame, text="The transaction is not successful, try again ", font=("Times", 20))
            label.grid(row=x, column=y)
            frame.after(1000, lambda: label.destroy())
            self.label_reservation = Label(
                frame, text="Would you like to reserve the book ?")
            self.label_reservation.grid(row=x + 1, column=y)
            self.button_yes = Button(frame, text="yes", command=lambda: [self.check_reservation_condition(
                checking_tuple, book_ID, frame, x, y), self.label_reservation.destroy(), self.button_no.destroy(), self.button_yes.destroy()],   font=("Times", 20))
            self.button_yes.grid(row=x + 2, column=y - 1)
            self.button_no = Button(frame, text="No ", command=lambda: frame.after(500, lambda: [
                                    self.label_reservation.destroy(), self.button_no.destroy(), self.button_yes.destroy()]),   font=("Times", 20))
            self.button_no.grid(row=x + 2, column=y + 1)

    # this function check if the the person that try to reserve the book is the same as the one that checked out

    def check_reservation_condition(self, checking_tuple, book_ID, frame, x, y):
        if checking_tuple[-1][4] != int(self.answer):
            self.d.update_reservation(book_ID, self.answer)
            label = Label(
                frame, text="The transaction is successful", font=("Times", 30))
            label.grid(row=x, column=y)
            frame.after(1000, lambda: label.destroy())
        else:
            label = Label(
                frame, text="The transaction is not successful, try again ", font=("Times", 30))
            label.grid(row=x, column=y)
            frame.after(1000, lambda: label.destroy())
