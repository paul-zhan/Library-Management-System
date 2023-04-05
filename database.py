import pandas as pd
import sqlite3
from tkinter.ttk import Treeview
from tkinter import *
from datetime import date


class Database:

    def __init__(self):

        # using pandas to read the file
        book_database = pd.read_csv('Book_Info.txt', sep='\t')
        self.book_database = book_database

        loan_database = pd.read_csv('Loan_Reservation_History.txt', sep='\t')
        self.loan_database = loan_database

        """in order to avoid redunduncy , we have to normalise the table into two tables
        the first table contains a table that contains book id , title and purchase date 
        the second table contains the table with  genre , title , author , purchase price
        """
        # creating table 1
        table1 = pd.DataFrame().assign(
            Book_ID=self.book_database['ID'], title=self.book_database['title'], purchase_date=self.book_database.iloc[:, -1:])
        self.table1 = table1
        # create table 2
        table2 = pd.DataFrame().assign(genre=self.book_database['Genre'], title=self.book_database['title'],
                                       author=self.book_database['Author '], purchase_price=self.book_database['Purchase Price £'])
        table2 = table2.drop_duplicates(keep='first')
        self.table2 = table2

        # establish a connection with the database if the data base exist good if not it creates a new one.
        db_conn = sqlite3.connect('library.db')
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()

        # Here we are converting a dataframe to a sql table
        self.book_database.to_sql(
            name='book', con=db_conn, if_exists='replace', index=False)
        self.loan_database.to_sql(
            name="reservation", con=db_conn, if_exists='replace', index=False)
        self.table1.to_sql(name="table1", con=db_conn,
                           if_exists='replace', index=False)
        self.table2.to_sql(name="table2", con=db_conn,
                           if_exists='replace', index=False)
        db_conn.commit()
        self.cursor.close()

        # import the date for the insertion
        self.current_time = date.today()
        self.current_time = self.current_time.strftime("%d/%m/%Y")

    def getting_books_bytitle(self, book_name, frame, x, y):
        """ this function will look into the database and see if the book name title we input is in the database.
     If it does it will return a list of elements similar to the input and display in a table (the tree object)
     note that : the search not case sensible so it will be more convenient to the user search

     Args:
            book_name : book title
            frame :  frame that the object will be display on 
            x : x location of the display table
            y : y location of the display table

     """

        self.cursor = self.db_conn.cursor()
        self.cursor.execute("""SELECT t1.Book_ID, t2.Genre , t1.title, t2.Author,t2.purchase_price, t1.purchase_date
                                FROM table1 t1
                                LEFT JOIN table2 t2 USING(title) 
                                WHERE t1.title LIKE ? COLLATE NOCASE""", ('%'+book_name+'%',))
        result = self.cursor.fetchall()

        if len(result) == 0:

            try:
                for book in self.tree.get_children():
                    self.tree.delete(book)
            except:
                print("It won't do anything because the database doesn't have it")

        else:
            # # define the columns
            columns = ("Book ID", "genre", "title", "author",
                       "purchase price £", "purchase date")
            self.tree = Treeview(frame, column=columns,
                                 show='headings', height=20)

            # define headings
            self.tree.heading("# 1", text="Book ID")
            self.tree.column("#1, width= 30")
            self.tree.heading("# 2", text="genre")
            self.tree.column("#2, width= 40")
            self.tree.heading("# 3", text="title")
            self.tree.column("#3, width= 75")
            self.tree.heading("# 4", text="author")
            self.tree.column("#4, width= 75")
            self.tree.heading("# 5", text="purchase price")
            self.tree.column("#5, width= 30")
            self.tree.heading("# 6", text="purchase date")
            self.tree.column("#6, width= 40")

            # add the data to the treeview
            for book in result:
                self.tree.insert("", END, values=book)

            # placing the table
            self.tree.grid(row=x, columnspan=y, sticky='nsew')
            self.cursor.close()

    # This function is similar to the function above, bu instead of searching by title it will search by genre.
    def getting_books_bygenre(self, genre, frame, x, y):
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("""SELECT t1.Book_ID, t2.Genre , t1.title, t2.Author,t2.purchase_price, t1.purchase_date
                                FROM table1 t1
                                LEFT JOIN table2 t2 USING(title) 
                                WHERE t2.genre LIKE ? COLLATE NOCASE""", ('%'+genre+'%',))

        result = self.cursor.fetchall()

        if len(result) == 0:
            try:
                for book in self.tree.get_children():
                    self.tree.delete(book)
            except:
                print("It won t do anything because the database doesn't have it")

        else:
            # define the columns
            columns = ("Book ID", "genre", "title", "author",
                       "purchase price £", "purchase date")
            self.tree = Treeview(frame, column=columns,
                                 show='headings', height=20)

            # define headings
            self.tree.heading("# 1", text="Book ID")
            self.tree.column("#1, width= 30")
            self.tree.heading("# 2", text="genre")
            self.tree.column("#2, width= 40")
            self.tree.heading("# 3", text="title")
            self.tree.column("#3, width= 75")
            self.tree.heading("# 4", text="author")
            self.tree.column("#4, width= 75")
            self.tree.heading("# 5", text="purchase price")
            self.tree.column("#5, width= 30")
            self.tree.heading("# 6", text="purchase date")
            self.tree.column("#6, width= 40")

            # add the data to the treeview
            for book in result:
                self.tree.insert("", END, values=book)

            # placing the table
            self.tree.grid(row=x, columnspan=y, sticky='nsew')
            self.cursor.close()

    # This function will fetch all the record of the book of the book specified
    def checking_book_status(self, book_ID):
        self.cursor = self.db_conn.cursor()
        self.cursor.execute(
            "SELECT * FROM reservation WHERE Book_ID = (?)", (book_ID,))
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    # This function will get the title from table1
    def checking_book_status_by_title(self, title):
        self.cursor = self.db_conn.cursor()
        self.cursor.execute(
            "SELECT * FROM table1 WHERE title = (?) COLLATE NOCASE ", (title,))
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def insert_data_database(self, book_ID, reservation_date, start_date, end_date, member_ID):
        """This function will insert values in the reservation table. 
            Args:
            book_ID : book ID
            reservation_date : date of the reservation / Null means that the book is not reserved 
            start_date : Date when the book is being checkout
            end_date : Date when the book is returned
            member_ID :  member ID of the user, it has to be 4 digits
        """
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("INSERT INTO reservation VALUES (?,?,?,?,?)",
                            (book_ID, reservation_date, start_date, end_date, member_ID))
        self.db_conn.commit()
        self.cursor.close()

    def update_data_database(self, book_ID):
        """
        This function will update the return date. 
        Args:
            book_ID : book ID 
        """
        self.cursor = self.db_conn.cursor()
        sql_update_query = """UPDATE reservation  SET  Return_Date = ?  WHERE Book_ID  = ? AND Checkout_Date IS NOT NULL """
        self.cursor.execute(sql_update_query, (self.current_time, book_ID))
        self.db_conn.commit()
        self.cursor.close()

    def insert_data_table1(self, book_ID, title):
        """
        This function is used to insert values in the table1
        Args:
            book_ID : book ID 
            member_ID :  member ID of the user, it has to be 4 digits
        """
        self.cursor = self.db_conn.cursor()
        self.cursor.execute("INSERT INTO table1 VALUES (?,?,?)",
                            (book_ID, title, self.current_time))
        self.db_conn.commit()
        self.cursor.close()

    def update_reservation(self, book_ID, member_ID):
        """
        This function is inserting values into the reservation table
        Args:
            book_ID : book ID 
            member_ID : title of the book
        """
        self.cursor = self.db_conn.cursor()
        sql_update_query = """ INSERT INTO reservation  VALUES  (?,?,?,?,?) """
        self.cursor.execute(
            sql_update_query, (book_ID, self.current_time, None, None, member_ID))
        self.db_conn.commit()
        self.cursor.close()

    def update_data_checkout(self, book_ID):
        """
        This function is used to update the checkout values in the reservation table
        Args:
            book_ID : book ID 

        """
        self.cursor = self.db_conn.cursor()
        sql_update_query = """UPDATE reservation  SET  Checkout_Date = ?  WHERE Book_ID  = ?  """
        self.cursor.execute(sql_update_query, (self.current_time, book_ID))
        self.db_conn.commit()
        self.cursor.close()

    def checking_return(self, book_ID):
        """
        This function will return the list where book_Id return date is null and the checkout date is not null
        Args:
            book_ID : book ID 

        """
        self.cursor = self.db_conn.cursor()
        self.cursor.execute(
            "SELECT * FROM reservation WHERE Book_ID = ?  AND Return_Date IS NULL AND  Checkout_Date IS NOT NULL", (book_ID,))
        result = self.cursor.fetchall()
        self.cursor.close()
        return result

    def recommendation_system(self, frame, x, y):
        """
        This function will fetch the top three borrowed book.
        Args:
            frame : frame that the thing gonna be displayed on 
            x :  x location of the recommendation table
            y : y location of the recommendation table

        """

        self.cursor = self.db_conn.cursor()
        self.cursor.execute("""SELECT  table1.title, table2.Author, count(table1.title) AS count
                                FROM table1 
                                INNER JOIN reservation ON  table1.Book_ID = reservation.Book_ID 
                                INNER JOIN  table2 ON table1.title = table2.title
                                GROUP BY table1.title  
                                HAVING count(table1.title) > 1
                                ORDER BY count(table1.title)  DESC """)
        # recommendation will be a list that contains the top three most borrowed book
        recommendation = self.cursor.fetchmany(3)
        columns = ("Title", "Author", "count")
        self.tree_recommendation = Treeview(
            frame, column=columns, show='headings', height=5)
        self.tree_recommendation.heading("# 1", text="Title")
        self.tree_recommendation.column("#1, width= 30", stretch=NO)
        self.tree_recommendation.heading("# 2", text="Author")
        self.tree_recommendation.column("#2, width= 40", stretch=NO)
        self.tree_recommendation.heading("# 3", text="borrowed times")
        self.tree_recommendation.column("#3, width= 75", stretch=NO)

        # looping through recommendation list to insert to the table
        for book in recommendation:
            self.tree_recommendation.insert("", END, values=book)

        self.tree_recommendation.grid(row=x, column=y)

        self.cursor.close()

        return recommendation
