from datetime import date
from book import Book
import db_util
import mysql.connector
from tabulate import tabulate
import util


class Order():

    @classmethod
    def place_order(cls, user_id, item_list, book_list):
        logger = util.get_logger()
        logger.info("place order")

        #calculate order value
        order_value = 0.0
        update_book_quantity_list = []
        for item in item_list:
            book_item_num = item[0]
            book_item_quantity = item[1]

            for book in book_list:
                book_num = book[1]

                if book_item_num == book_num:    
                    book_price = book[4]
                    book_quantity = book[5]

                    order_value = (book_price * book_item_quantity) + order_value
                    update_book_quantity_list.append((book_num, (book_quantity-book_item_quantity)))

            logger.info("total order price: " + str(order_value))
            logger.info(update_book_quantity_list)

        # insert into UserOrder table
        # get db connection

        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        today = date.today()
        date_string = today.strftime("%Y-%m-%d")
        add_order = "INSERT INTO UserOrder (OrderValue, OrderDate, UserID) VALUES (" + str(order_value) + ", '" + date_string + "', " + str(user_id) + ");"
        #print(add_order)
        logger.info(add_order)

        db_cursor.execute(add_order)
        database_cnx.commit()

        #get order ID
        order_id = db_cursor.lastrowid

        #insert into OrderItem table
        for item in item_list:
            book_item_num = item[0]
            book_item_quantity = item[1]

            add_order_item = "INSERT INTO OrderItem (OrderID, BookNum, Quantity) VALUES (" + str(order_id) + ", '" + book_item_num + "', " + str(book_item_quantity) + ");"

            logger.info(add_order_item)
            db_cursor.execute(add_order_item)
            database_cnx.commit()

        #close db connection
        db_cursor.close()
        database_cnx.close()

        #update book quantity
        for book in update_book_quantity_list:
            book_num = book[0]
            new_book_quantity = book[1]
            Book.update_book_quantity(book_num, new_book_quantity)

        return order_id
    
    @classmethod
    def get_order_details(self, order_id):
        logger = util.get_logger()
        logger.info("Get all orders")

         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        # get order details
        order_query = "SELECT OrderID, OrderValue, OrderDate FROM UserOrder WHERE OrderID = " + str(order_id) + ";"
        db_cursor.execute(order_query)
        logger.info(order_query)
   
        order_result = db_cursor.fetchall()
        #print(order_result)
        logger.info(order_result)


        # get order items
        item_query = "SELECT b.Title, b.Price, o.Quantity FROM OrderItem o, Book b WHERE o.BookNum = b.BookNum AND OrderID = " + str(order_id) + ";"
        db_cursor.execute(item_query)
        logger.info(item_query)
        
   
        item_result = db_cursor.fetchall()
        #print(item_result)
        logger.info(item_result)

        print("\n========================== Your Order ============================\n")

        print("Order ID: " + str(order_result[0][0]))
        print("Total Price: $" + str(order_result[0][1]))
        print("Order Date: " + str(order_result[0][2]))
        print("\n")
        
        headers = ["Book Title", "Unit Price", "Quantity"]
        print(tabulate(item_result, headers = headers))

        print("\n==================================================================\n")

        #close db connection
        db_cursor.close()
        database_cnx.close()

        logger.info("Done getting order details")




    @classmethod
    def get_orders_by_user(cls, user_id):
        logger = util.get_logger()
        logger.info("Get all orders for single user")

         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        # get order details
        get_user_order_query = "SELECT * FROM UserOrder WHERE UserID = " + str(user_id) + ";"
        db_cursor.execute(get_user_order_query)
        logger.info(get_user_order_query)
   
        get_user_order_result = db_cursor.fetchall()
        #print(get_user_order_result)
        logger.info(get_user_order_result)

        print("\n========================== Your Previous Orders ============================\n")
        
        headers = ["Order ID", "Order Value", "Order Date", "User ID"]
        print(tabulate(get_user_order_result, headers = headers))

        print("\n===========================================================================\n")

        #close db connection
        db_cursor.close()
        database_cnx.close()

        logger.info("Done getting all orders for single user")

        return get_user_order_result

    @classmethod
    def get_all_orders(cls):
        logger = util.get_logger()
        logger.info("Get all orders for all users")

         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        # get order details
        get_all_user_order_query = "SELECT p.UserID, p.UserName, u.OrderID, u.OrderValue, u.OrderDate FROM UserOrder u, Person p WHERE u.UserID = p.UserID ORDER BY UserName;"
        db_cursor.execute(get_all_user_order_query)
        logger.info(get_all_user_order_query)
   
        get_user_order_result = db_cursor.fetchall()
        #print(get_user_order_result)
        logger.info(get_user_order_result)

        print("\n========================== Previous Orders ============================\n")
        
        headers = ["User ID", "User Name", "Order ID", "Total Price", "Order Date"]
        print(tabulate(get_user_order_result, headers = headers))

        print("\n===========================================================================\n")

        #close db connection
        db_cursor.close()
        database_cnx.close()

        logger.info("Done getting all orders for all users")


#test place order
'''test_user_id = 1
item_list = [('1004', 3),('1001', 2)]
book_list = [(1, '1001', 'The Lord of the Rings', 'J. R. R. Tolkien', 20.5, 10), 
             (2, '1002', 'Pride and Prejudice', 'Jane Austen', 10.2, 15),
              (3, '1003', 'The Lion, The Witch, and the Wardrobe', 'C.S. Lewis', 5.6, 8), 
              (4, '1004', 'Macbeth', 'William Shakespeare', 3.5, 20), 
              (5, '1005', 'The Odyssey', 'Homer', 30.2, 1)]
Order.place_order(test_user_id, item_list, book_list)'''

#Order.get_order_details(11)

#Order.get_orders_by_user(1)

#Order.get_all_orders()
