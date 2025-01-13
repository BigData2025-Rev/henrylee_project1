'''
Book Store app
'''

import sys

from book import Book
from order import Order
from user import User, BookStoreUser, BookStoreAdmin
import util
  
logger = util.get_logger()

def bookstore_menu(user): 
    logger = util.get_logger()
    option = True
    print("\nWelcome to Henry's Book Store " + user.get_full_name() + "\n")

    while option: 
        #list all books
        print("1. Buy Books")
        print("2. View Past Orders")
        print("3. Exit\n")

        menu_selection = input("Enter your option: \n")
        if menu_selection == "1":
            item_list= []
            book_list = Book.get_all_books()
            while True:
                action = input("\nEnter 1 to add a book to your cart, 2 to checkout, or 0 to exit to main menu: ")
                if action == "2":
                    #checkout cart
                    logger.info("checkout cart")
                    
                    #place order
                    order_id = Order.place_order(user.user_id, item_list, book_list)
                    
                    #get order details
                    Order.get_order_details(order_id)
                    break
                elif action == "1": 
                    # add book to cart
                    logger.info("add a book to the cart")
                    book_number = input("Please enter a book's number: ")
                    book_quantity = int(input("Enter the number of copies: "))

                    item = (book_number, book_quantity)
                    item_list.append(item)
                else:
                    break

        elif menu_selection == "2":
            #show past orders
            logger.info("show past orders")
            user_id = user.user_id
            Order.get_orders_by_user(user_id)

            while True:
                action = input("Enter 1 to view order details, or enter 2 to go back to main menu: ")
                if action == "1":
                    order_id = input("Enter an order ID: ")
                    logger.info("show order details")
                    Order.get_order_details(order_id)
                elif action == "2":
                    logger.info("return to main menu")
                    break
                else:
                    print("Invalid option")

        elif menu_selection == "3":
            logger.info("exit store")
            print("\n Thank you for visiting. See you next time!\n")
            return False
        else:
            print("Invalid choice\n")
            return False

def bookstore_menu_admin(user):
    print("\nWelcome to the Book Store's Admin Page " + user.get_full_name() + "\n")

    option = True
    while option: 
        print("1. Update Book Catalog")
        print("2. Manage Users")
        print("3. View All Orders")
        print("0. Exit\n")

        menu_selection = input("Enter your option: ")
        if menu_selection == "1":
            print("update book ")
            #list all books
            logger.info("update book catalog")
            Book.get_all_books()

            while True:
                print("Update Book Catalog: ")
                print("1. Add a new book")
                print("2. Delete a book")
                print("3. Update Book Price")
                print("4. Update Book Quantity")
                print("0. Back to main menu\n")
                sub_menu_selection = input("Enter your option: ")

                if sub_menu_selection == "1":
                    #add new book
                    logger.info("add new book")
                    print("Enter a book's information to add")
                    book_id = input("Book ID: ")
                    title = input("Title: ")
                    author = input("Author: ")
                    price = input("Price: ")
                    quantity = input("Quantity: ")

                    new_book = Book(book_id, title, author, price, quantity)
                    new_book.add_book()

                    #list all books
                    Book.get_all_books()
                elif sub_menu_selection == "2":
                    #remove a book
                    logger.info("remove a book")
                    print("Enter a book's ID to delete")
                    book_id = input("Book ID: ")
                    Book.remove_book(book_id)

                    #list all books
                    Book.get_all_books()
                elif sub_menu_selection == "3":
                    #update book price
                    logger.info("update book price")
                    print("Enter a book's number and price to update its price")
                    book_id = input("Book Number: ")
                    book_price = input("Book Price: ")
                    print("\n")
                    Book.update_book_price(book_id, book_price)
                elif sub_menu_selection == "4":
                    #update book quantity
                    logger.info("update book quantity")
                    print("Enter a book's number and quantity to update its quantity")
                    book_id = input("Book Number: ")
                    book_quantity = input("Book Quantity: ")
                    print("\n")
                    Book.update_book_quantity(book_id, book_quantity)
                elif sub_menu_selection == "0":
                    #go back to main menu
                    logger.info("return to main menu")
                    break
                else:
                    print("Invalid choice\n")

        elif menu_selection == "2":
            print("manage users")
            #list all users
            logger.info("manage users")
            user.get_all_users()

            while True:
                print("Manage Users: ")
                print("1. Add a new user")
                print("2. Remove a user")
                print("3. Grant admin access to user")
                print("0. Back to main menu\n")
                sub_menu_selection = input("Enter your option: ")

                if sub_menu_selection == "1":
                    #add user
                    logger.info("add a new user")
                    print("Please enter user information: ")
                    username = input("User Name: ")
                    password = input("Password: ")
                    fname = input("First Name: ")
                    lname = input("Last Name: ")
                    role = input("Role (user or admin): ")

                    user.add_user(fname, lname, username, password, role)
                    user.get_all_users()
                elif sub_menu_selection == "2":
                    #remove user
                    logger.info("remove a user")
                    print("Please enter a user to remove")
                    user_id = input("User ID: ")
                    user.remove_user(user_id)

                    #list all current users
                    user.get_all_users()
                elif sub_menu_selection == "3":
                    #grant admin access to user
                    logger.info("grant user admin access")
                    print("Enter a user's username to grant admin access")
                    username = input("User Name: ")
                    user.grant_admin_access(username)
                elif sub_menu_selection == "0":
                    logger.info("return to main menu")
                    break
                else: 
                    print("Invalid Choice\n")
        
        elif menu_selection == "3":
            #show all past orders
            logger.info("show all past orders")
            Order.get_all_orders()

            while True:
                action = input("Enter 1 to view order details, or enter 2 to go back to main menu: ")
                if action == "1":
                    order_id = input("Enter an order ID: ")
                    logger.info("show order details")
                    Order.get_order_details(order_id)
                elif action == "2":
                    logger.info("return to main menu")
                    break
                else:
                    print("Invalid option")

        elif menu_selection == "0":
            logger.info("log out of account")
            print("\nLogged Out. See you next time!\n")
            return False
        else:
            print("Invalid choice\n")


def login():
    print("\nWelome to Henry's Book Store!")
    print("\nPlease enter your user name and password to login ")
    user_name = input("User Name: ")
    password = input("Password: ")

    logger.info("log into user account")
    user_record = User.login(user_name, password) 
    logger.info(user_record)
    if len(user_record) == 0:
        print("User not found.")
        sys.exit()
    else:
        #User found
        user_id = user_record[0][0]
        username = user_record[0][1]
        fname = user_record[0][2]
        lname = user_record[0][3]
        user_role = user_record[0][4]
        if user_role == 'user':
            logger.info("Login as a bookstore user")
            return BookStoreUser(user_id, fname, lname, username)
        else:
            logger.info("Login as an admin user")
            return BookStoreAdmin(user_id, fname, lname, username)

def signup():
    #logger = util.get_logger()
    logger.info("Create a new user account")
    print("\nWelome to Henry's Book Store!")
    print("\nPlease enter a user name and password to sign up ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    user_name = input("User Name: ")
    password = input("Password: ")
    BookStoreUser.add_user(first_name, last_name, user_name, password)
    

def main():
    print("Welcome to Henry's Book Store!")
    print("\n")
    user_option = input("Press 1 to log in with existing account or 2 to sign up for a new account: ")
    if user_option == "1":
        logger.info("log into account")
        login_user = login()
        if isinstance(login_user, BookStoreUser):
            logger.info("log in as user")
            bookstore_menu(login_user)
        else:
            logger.info("log in as admin")
            bookstore_menu_admin(login_user)
    elif user_option == "2":
        #sign up for new account
        logger.info("create new account")
        signup()

        #login after sign up
        logger.info("log into account")
        login_user = login()
        if isinstance(login_user, BookStoreUser):
            logger.info("log in as user")
            bookstore_menu(login_user)
        else:
            logger.info("log in as admin")
            bookstore_menu_admin(login_user)
    else:
        print("Please enter a valid option")
    
    #bookstore_input = input("Enter your option: ")
    #bookstore_menu(bookstore_input)
    

if __name__ =="__main__":
    main()


