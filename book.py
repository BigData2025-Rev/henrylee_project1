from datetime import date
import db_util
import mysql.connector
from tabulate import tabulate
import util

class Book():
    logger = util.get_logger()

    def __init__(self, book_number, book_title, book_author, book_price, book_quantity):
        self.book_number = book_number
        self.book_title = book_title
        self.book_author = book_author
        self.book_price = book_price
        self.book_quantity = book_quantity

    @classmethod
    def get_all_books(cls):
        Book.logger.info("Get all books")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT * FROM Book;"
        db_cursor.execute(query)
        Book.logger.info(query)
   
        my_result = db_cursor.fetchall()
        #print(my_result)
        Book.logger.info(my_result)

        print("\n========================== Book Catalog ============================\n")
        
        headers = ["Book ID", "BookNum", "Title", "Author", "Price", "Quantity"]
        print(tabulate(my_result, headers = headers))

        print("\n=================================================================\n")

        #close db connection
        db_cursor.close()
        database_cnx.close()

        Book.logger.info("Done getting all books")
        return my_result
    
   
       #add book to catalog
    def add_book(self):
        Book.logger.info("add book")
        # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT BookID FROM Book WHERE BookNum = '" + self.book_number + "'"
        db_cursor.execute(query)
        Book.logger.info(query)
   
        my_result = db_cursor.fetchall()
        #print(my_result)

        if len(my_result) == 0:
            # if user doesn't exist, then add
            add_book = "INSERT INTO Book (BookNum, Title, Author, Price, Quantity) VALUES ('" + self.book_number + "', '" + self.book_title + "', '"+ self.book_author  + "', '"+ self.book_price + "', '" + self.book_quantity + "'); "
            #print(add_book)
            Book.logger.info(add_book)
            db_cursor.execute(add_book)
            database_cnx.commit()
            print("\n Book " + self.book_title + " is added.")
        else:
            print("\n Book " + self.book_title + " already exists.")
        
        #close db connection
        db_cursor.close()
        database_cnx.close()

    
    #remove book by book number
    @classmethod
    def remove_book(self, book_number):
        Book.logger.info("remove book")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        book_item = "SELECT * FROM OrderItem WHERE BookNum = '" + book_number + "';"
        Book.logger.info(book_item)
        db_cursor.execute(book_item)
        
        my_result = db_cursor.fetchall()

        if len(my_result) == 0:
            #check if book exists
            delete_book = "DELETE FROM Book WHERE BookNum = '" + book_number + "';"
            #print(query)
            Book.logger.info(delete_book)
            db_cursor.execute(delete_book)
            database_cnx.commit()
            
            #close db connection
            db_cursor.close()
            database_cnx.close()

            print( book_number + " has been deleted")
        else:
            print( book_number + " can not be deleted")


    @classmethod
    def update_book_quantity(self, book_number, book_quantity):
        Book.logger.info("update book quantity")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        update_quantity = "UPDATE Book SET Quantity = '" + str(book_quantity) + "' WHERE  BookNum = '" + book_number + "'"
        #print(update_quantity)
        Book.logger.info(update_quantity)
        db_cursor.execute(update_quantity)
        database_cnx.commit()
        
        #close db connection
        db_cursor.close()
        database_cnx.close()

        print(book_number + " quantity updated\n")


    @classmethod
    def update_book_price(self, book_number, book_price):
        Book.logger.info("update book price")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        update_price = "UPDATE Book SET Price = " + book_price + " WHERE  BookNum = '" + book_number + "'"
        #print(update_quantity)
        Book.logger.info(update_price)
        db_cursor.execute(update_price)
        database_cnx.commit()
        
        #close db connection
        db_cursor.close()
        database_cnx.close()

        print(book_number + " price updated\n")



####### Test Cases #######

'''u1 = BookStoreUser("Helen", "Lee", "helen")
Book.get_all_books(u1)'''

#u2 = BookStoreAdmin("Amy", "Lee", "alee")
#Book.get_all_books(u2)

#add a book
#book1 = Book("10001", "Python in Action", "ABC Author", "20.50", "5")
#book1.add_book()
#Book.get_all_books(u2)

#remove a book
#Book.remove_book("10001")
#Book.get_all_books(u2)

#update book quantity
#Book.update_book_quantity("10001", "3")

#update book price
#Book.update_book_price("10001", "15.55")
