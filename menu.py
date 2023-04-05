from tkinter import *
from bookCheckout import BookCheckout
from bookSearch import Booksearch
from bookReturn import BookReturn
from bookSelect import BookSelect
from PIL import ImageTk, Image


class Menu:

    def __init__(self):
        # initialise all the variable that I need for this class mostly
        self.bookcheckout = BookCheckout()
        self.booksearch = Booksearch()
        self.bookreturn = BookReturn()
        self.bookselect = BookSelect()

        # importing images and resizing it
        image = Image.open("back_button.jpg")
        image = image.resize((60, 60), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)

        buy_image = Image.open("buy_icon.jpg")
        buy_image = buy_image.resize((60, 60), Image.ANTIALIAS)
        self.buy = ImageTk.PhotoImage(image=buy_image)

    def main_frame(self, window):
        """This function will contains the main frame and also all the other frame.

        Args:
            window : tk window
        """
        # =========================  main frame ===============================

        frame = Frame(window, bg="black", width=1000, height=750)
        frame.pack()
        frame.pack_propagate(0)

        label = Label(frame, text="Welcome to popo Library")
        label.config(font=("Times", 40))
        label.pack(side=TOP)

        button_for_booksearch = Button(frame, text="Searching for Books",
                                       command=lambda: self.switch_frame(frame, booksearch_frame), font=("Times", 30))
        button_for_booksearch.pack(
            side=TOP, fill=BOTH, expand=TRUE, padx=10, pady=10)

        button_for_checkingoutbooks = Button(frame, text="Checking out Books",
                                             command=lambda: self.switch_frame(frame, checkout_frame), font=("Times", 30))
        button_for_checkingoutbooks.pack(
            side=TOP,  fill=BOTH, expand=TRUE,  padx=10, pady=10)

        button_for_returningbooks = Button(frame, text="Returning books",
                                           command=lambda: self.switch_frame(frame, return_frame), font=("Times", 30))
        button_for_returningbooks.pack(
            side=TOP,  fill=BOTH, expand=TRUE,  padx=10, pady=10)

        button_for_purchaseOrder = Button(frame, text="Purchase new books",
                                          command=lambda: self.switch_frame(frame, purchase_frame), font=("Times", 30))
        button_for_purchaseOrder.pack(
            side=TOP,  fill=BOTH, expand=TRUE,  padx=10, pady=10)

        button_quit = Button(frame, text="Quit",
                             command=window.destroy, font=("Times", 30))
        button_quit.pack(side=TOP,  fill=BOTH, expand=TRUE,  padx=10, pady=10)

        # ======================== booksearch frame ==========================

        booksearch_frame = Frame(window, width=1000, height=750)
        frame.pack_propagate(0)

        label = Label(booksearch_frame, text="BookSearch", font=("Times", 30))
        label.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

        go_back_button = Button(booksearch_frame, image=self.image,
                                command=lambda: [self.switch_frame(booksearch_frame, frame)], font=("Times", 30))
        go_back_button.grid(row=0, column=0, padx=10, pady=10)

        label_search = Label(
            booksearch_frame, text="Search by", font=("Times", 30))
        label_search.grid(row=1, column=0, padx=10, pady=10)

        search_var = StringVar()
        search_var.set("title")

        search_choice = OptionMenu(
            booksearch_frame, search_var, "title", "genre")
        search_choice.grid(row=1, column=1, padx=10, pady=10)

        self.book_name = Entry(booksearch_frame, font=("Times", 30))
        self.book_name.grid(row=1, column=3, padx=10, pady=10)

        validate_button = Button(booksearch_frame, text="search",
                                 command=lambda: (self.booksearch.search(self.book_name.get(), booksearch_frame, 6, 5, search_var.get())), font=("Times", 30))
        validate_button.grid(row=1, column=4, padx=10, pady=10)

        # ====================== checkout frame ============================

        checkout_frame = Frame(window, bg="black", width=1000, height=750)
        frame.pack_propagate(0)

        checkout_label = Label(checkout_frame, text="Checkout", font=("Times", 30))
        checkout_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        go_back_button = Button(checkout_frame, image=self.image,
                                command=lambda: self.switch_frame(checkout_frame, frame), font=("Times", 20))
        go_back_button.grid(row=0, column=0, padx=10, pady=10)

        member_id_label = Label(
            checkout_frame, text="Please enter your member ID", font=("Times", 30))
        member_id_label.grid(row=1, column=1, padx=10, pady=10)

        member_id_entry = Entry(checkout_frame, font=("Times", 30))
        member_id_entry.grid(row=2, column=1, padx=10, pady=10)

        book_id_label = Label(
            checkout_frame, text="Please enter the book ID you want to borrow", font=("Times", 30))
        book_id_label.grid(row=3, column=1, padx=10, pady=10)

        self.book_id_entry = Entry(checkout_frame, font=("Times", 30))
        self.book_id_entry.grid(row=4, column=1, padx=10, pady=10)

        confirm_button = Button(checkout_frame, text="Confirm",
                                command=lambda: [self.bookcheckout.check_memberID(member_id_entry.get(), self.book_id_entry.get(), checkout_frame, 0, 1)], font=("Times", 20))
        confirm_button.grid(row=5, column=1, padx=10, pady=10)

        # ====================== return frame ============================

        return_frame = Frame(window, bg="black", width=1000, height=750)

        book_id_label = Label(
            return_frame, text="please enter the book ID you want to return",  font=("Times", 30))
        book_id_label.grid(row=0, column=1, padx=10, pady=10)

        book_id_entry = Entry(return_frame,  font=("Times", 30))
        book_id_entry.grid(row=1, column=1, padx=10, pady=10)

        go_back_button = Button(return_frame, image=self.image, command=lambda: self.switch_frame(
            return_frame, frame), font=("Times", 30))
        go_back_button.grid(row=0, column=0, padx=10, pady=10)

        confirm_button = Button(return_frame, text="confirm", command=lambda: self.bookreturn.returnBook(
            book_id_entry.get(), return_frame, 4, 1), font=("Times", 30))
        confirm_button.grid(row=3, column=1, padx=10, pady=10)

        # ======================  purchase frame ================================

        purchase_frame = Frame(window,  bg="black")

        book_id_label = Label(
            purchase_frame, text="Top pick for you", font=("Times", 30))
        book_id_label.grid(row=0, column=1, padx=5, pady=10)

        self.bookselect.get_recommendation(purchase_frame, 1, 1)

        go_back_button = Button(purchase_frame, image=self.image, command=lambda: self.switch_frame(
            purchase_frame, frame), font=("Times", 20))
        go_back_button.grid(row=0, column=0, padx=5, pady=5)

        asking_label = Label(
            purchase_frame, text="Please enter the book you want to buy", font=("Times", 30))
        asking_label.grid(row=4, column=1, padx=5, pady=5)

        book_entry = Entry(purchase_frame, font=("Times", 30))
        book_entry.grid(row=5, column=1, padx=5, pady=5)

        button_validate = Button(purchase_frame, image=self.buy, command=lambda: [
                                 self.bookselect.buying_books(book_entry.get(), purchase_frame, 5, 3)], font=("Times", 30))
        button_validate.grid(row=5, column=2, padx=5, pady=5)

    # function that allow the user to swich frame by forgetting the current one and pack the new one.
    def switch_frame(self, frame1, frame2):
        frame1.forget()
        frame2.pack()


if __name__ == "__main__":
    # creating a tkinter object
    window = Tk()
    # setting the title 
    window.title("library management")
    # make the window background black
    window.configure(bg="black")
    window.geometry("1200x750")
    menu = Menu()

    menu.main_frame(window)
    window.mainloop()












