import db_util
import mysql.connector
from tabulate import tabulate

from order import Order
import util

class User():
    logger = util.get_logger()
    firstname = ''
    lastname = ''
    username = ''
    password = ''
    user_id = 0

    def __init__(self, user_id, fname, lname, uname) -> None:
        self.user_id = user_id
        self.firstname = fname
        self.lastname = lname
        self.username = uname
    
    def print_full_name(self):
        print(f"{self.lastname}, {self.firstname}\n")
    
    def get_full_name(self):
        return self.firstname + " " + self.lastname
    
    @classmethod
    def login(cls, user_name, password):
        User.logger.info("User log in")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT UserID, UserName, FirstName, LastName, Role FROM Person WHERE UserName = '" + user_name + "' AND Password = '" + password + "';  "
        db_cursor.execute(query)
        User.logger.info(query)
   
        user_result = db_cursor.fetchall()
        #print(my_result)

        #close db connection
        db_cursor.close()
        database_cnx.close()

        User.logger.info("finished logging in")
        return user_result

class BookStoreUser(User):
    role = "user"

    def __init__(self, user_id, fname, lname, uname) -> None:
        super().__init__(user_id, fname, lname, uname)


    # add new user
    @classmethod
    def add_user(self, fname, lname, uname, password):
        User.logger.info("adding user")
        # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT UserID FROM Person WHERE UserName = '" + uname + "'"
        db_cursor.execute(query)
        User.logger.info(query)
   
        my_result = db_cursor.fetchall()
        User.logger.info(my_result)
        #print(my_result)
       
        if len(my_result) == 0:
            # if user doesn't exist, then add
            add_person = "INSERT INTO Person (UserName, Password, FirstName, LastName, Role) VALUES ('" + uname + "', '" + password + "', '"+ fname  + "', '"+ lname + "', '" + self.role + "'); "
            #print(add_person)
            db_cursor.execute(add_person)
            User.logger.info(add_person)
            database_cnx.commit()
            print("\n User " + fname + " " + lname + " is added. Please log in.")
        else:
            print("\n User " + fname + " " + lname + " already exists. Please log in.")
        
        #close db connection
        db_cursor.close()
        database_cnx.close()




class BookStoreAdmin(User):
    role = "admin"

    def __init__(self, user_id, fname, lname, uname) -> None:
        super().__init__(user_id, fname, lname, uname)

    # get all users
    def get_all_users(self):
        User.logger.info("get all users")
        # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT UserID, UserName, FirstName, LastName, Role FROM Person;"
        db_cursor.execute(query)
        User.logger.info(query)

        my_result = db_cursor.fetchall()
        User.logger.info(my_result)
        #print(my_result)

        print("\n========================== All Users ============================\n")
        
        headers = ["User ID", "User Name", "First Name", "Last Name", "Role"]
        print(tabulate(my_result, headers = headers))

        print("\n=================================================================\n")

        #close db connection
        db_cursor.close()
        database_cnx.close()
    

    # add new user
    def add_user(self, fname, lname, uname, password, role):
        User.logger.info("add user")
        # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "SELECT UserID FROM Person WHERE UserName = '" + uname + "'"
        db_cursor.execute(query)
        User.logger.info("query")
   
        my_result = db_cursor.fetchall()
        #print(my_result)
       
        if len(my_result) == 0:
            # if user doesn't exist, then add
            add_person = "INSERT INTO Person (UserName, Password, FirstName, LastName, Role) VALUES ('" + uname + "', '" + password + "', '"+ fname  + "', '"+ lname + "', '" + role + "'); "
            #print(add_person)
            User.logger.info(add_person)
            db_cursor.execute(add_person)
            database_cnx.commit()
            print("\n User " + fname + " " + lname + " is added.")
        else:
            print("\n User " + fname + " " + lname + " already exists.")
        
        #close db connection
        db_cursor.close()
        database_cnx.close()


    # remove user
    def remove_user(self, user_id):
        User.logger.info("remove user")
         # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        user_order = Order.get_orders_by_user(user_id)
        #check if user exists, if doesn't exist then delete
        if len(user_order) == 0:
            query = "DELETE FROM Person WHERE UserID = '" + user_id + "'"
            #print(query)
            User.logger.info(query)
            db_cursor.execute(query)
            database_cnx.commit()
            
            #close db connection
            db_cursor.close()
            database_cnx.close()

            print("User has been deleted")
        else:
            print("User has orders and cannot be deleted")


    def grant_admin_access(self, uname):
        User.logger.info("grant admin access")
        # get db connection
        database_cnx = db_util.get_database_connection()
        db_cursor = database_cnx.cursor()

        #check if user exists
        query = "UPDATE Person SET Role = 'admin' WHERE  UserName = '" + uname + "'"
        #print(query)
        User.logger.info(query)
        db_cursor.execute(query)
        database_cnx.commit()
        
        #close db connection
        db_cursor.close()
        database_cnx.close()

        print( uname + " granted admin access\n")
   

####### Test Cases #########

###test print user name
'''user1 = User('amy','lee','alee')
user1.print_full_name()
print(user1.get_full_name())'''

###test login
#user = User.login("george", "test456")
#print(user)
#User.login("abc","user123")

#test adding/removing user
#user1 = BookStoreAdmin(1, "amy", "lee", "alee") 

#get all users
#user1.get_all_users()

#add new admin user
#user1.add_user("Adam", "Johnson", "adam", "test123", "admin")
#user1.get_all_users()

#test grant user admin access
#user1.grant_admin_access("adam")

#test remove user by user name
#user1.remove_user("adam")

#user1.get_all_users()

#user2 = BookStoreUser("George", "Franklin", "george")
#user2.add_user("George", "Franklin", "george", "test456")

