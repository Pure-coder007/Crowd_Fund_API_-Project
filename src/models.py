import mysql.connector  
from .database import config
from datetime import datetime


class User():
    def __init__(self, id, first_name, last_name, email, password, is_admin=False):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin


        @classmethod
        def get(cls, user_id):
            pass


def add_user(first_name, last_name, email, password, is_admin=False):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO user(first_name, last_name, email, password, is_admin) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, email, password, is_admin))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()
    



def get_user_by_id(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user WHERE id=%s', (user_id,))
    user_record = cursor.fetchone()
    cursor.close()
    connection.close()

    if user_record:
        return User(id=user_record['id'], first_name=user_record['first_name'], last_name=user_record['last_name'], email=user_record['email'], password=user_record['password'], is_admin=user_record['is_admin'])
    return None





# Getting a user logged in
# def get_user(email):
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM user WHERE email=%s', (email,))
#     user_record = cursor.fetchone()
#     cursor.close()
#     connection.close()

#     if user_record:
#         return User(id=user_record['id'], first_name=user_record['first_name'], last_name=user_record['last_name'], email=user_record['email'], password=user_record['password'], is_admin=user_record['is_admin'])
#     return None
def get_user(email):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute('SELECT * FROM `final_fund`.`user` WHERE email=%s', (email,))

        user_record = cursor.fetchone()
        
        if user_record:
            return User(
                id=user_record['id'],
                first_name=user_record['first_name'],
                last_name=user_record['last_name'],
                email=user_record['email'],
                password=user_record['password'],
                is_admin=user_record['is_admin']
            )
        return None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if cursor: cursor.close()
        if connection: connection.close()







# Adding a category to the database
def add_category(user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount, balance):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    try:
        # Validate and parse the expiry_date
        if not expiry_date:
            # Handle the case where expiry_date is empty or None
            raise ValueError('Expiry date is required')
        
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d')
        
        insert_query = """
        INSERT INTO categories (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount, balance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    
        # Assuming you have access to the user's email or can obtain it
        # user_email = get_user_email_by_id(user_id)
        
        values = (user_id, category_name, fundraising_for, expiry_date, amount, description, minimum_amount, balance)
        cursor.execute(insert_query, values)
        connection.commit()
        cursor.close()
        connection.close()

    except ValueError as e:
        # Handle invalid date format or missing date
        print(f"Error adding category: {str(e)}")

    except Exception as e:
        # Handle other database or general errors
        print(f"Error adding category: {str(e)}")

    

def fetch_category_by_id(category_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True) 
    query = """
    SELECT * FROM categories
    WHERE user_id = %s
    """
    cursor.execute(query, (category_id,))
    cat = cursor.fetchone()
    return cat


# Getting all categories
def add_request(user_email, category_name, fundraising_for, expiry_date, amount, description, minimum_amount):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # SQL INSERT statement
        insert_query = """
        INSERT INTO pend_requests (user_email, category_name, fundraising_for, expiry_date, amount, description, minimum_amount)
        VALUES ( %s, %s, %s, %s, %s, %s, %s)
        """

        # Values to insert into the table
        values = (user_email, category_name, fundraising_for, expiry_date, amount, description, minimum_amount)

        cursor.execute(insert_query, values)
        connection.commit()
        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return False
    return True




# Getting all categories
def get_all_requests():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT id, user_email, category_name, fundraising_for, expiry_date, amount, description, approved, minimum_amount FROM pend_requests')

        requests = cursor.fetchall()
        cursor.close()
        connection.close()
        return requests
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return []
    

def get_minimum_amount():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT minimum_amount FROM categories LIMIT 1')

    request = cursor.fetchone()
    cursor.close()
    connection.close()
    if request:
        return float(request['minimum_amount'])
    return None



def get_all_approved_requests():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM pend_requests WHERE approved = 1")
    approved_requests = cursor.fetchall()

    cursor.close()
    connection.close()
    return approved_requests




# Sowing a user his request
def get_user_requests(user_id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        # Retrieve requests for the current user based on their user ID
        select_query = """
        SELECT category_name, fundraising_for,  amount, description FROM categories WHERE user_id = %s
        """
        print(user_id, 'userid')
        cursor.execute(select_query, (user_id,))
        user_requests = cursor.fetchall()
        print(user_requests, 'userrequest')
        return user_requests

    except Exception as e:
        print(f"Error fetching user requests: {str(e)}")
        return []

    finally:
        cursor.close()
        connection.close()





def is_user_admin(email):
    user = get_user(email)
    return user.is_admin if user else False



 
# Getting all approved requests
def set_request_status(request_id, status, user_email, category_name, fundraising_for, expiry_date, amount):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO approved_requests (id, status, user_email, category_name, fundraising_for, expiry_date, amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (request_id, status, user_email, category_name, fundraising_for, expiry_date, amount))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

def requests_for_donators(user_email, category_name, amount, description):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    try:
        insert_query = """
            INSERT INTO donator_view(user_email, category_name, amount, description)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_email, category_name, amount, description))

        connection.commit()

        return True

    except mysql.connector.Error as err:
        print("Error:", err)
        return False

    finally:
        cursor.close()
        connection.close()


def add_donation(amount_donated, donator_name, required_amount, email, cat_id):
    connection = mysql.connector.connect(**config)
   
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO donations_info (amount_donated, donator_name, required_amount, email, cat_id)
    VALUES (%s, %s, %s, %s, %s)
    """
    # data = (amount_donated, donator_name, required_amount, email, cat_id)
    cursor.execute(insert_query, (amount_donated, donator_name, required_amount, email, cat_id))
    connection.commit()
    cursor.close()
    connection.close()
    print('Donation added successfully')
    return True
    

def query_cat_id(cat_id:int):
    print('i am here')
    connection = mysql.connector.connect(**config)
    print('i am here')
    print(cat_id)

    cursor = connection.cursor()
    print('i am here')
    select_query = """SELECT * FROM donations_info WHERE cat_id = %s"""
    print('i am here')
    cursor.execute(select_query, (cat_id,))
    print('i am here')
    user_requests = cursor.fetchall()
    print('i am here')
    print(user_requests, 'userrequest')
    return user_requests

def fetch_cat(cat_id):
    connection = mysql.connector.connect(**config)
    print(cat_id)

    cursor = connection.cursor()
    select_query = """
    SELECT * FROM categories WHERE id = %s
"""
    cursor.execute(select_query, (cat_id,))
    user_requests = cursor.fetchone()
    print(user_requests, 'userrequest')
    return user_requests




# Showing the donator all donations
def get_all_donations():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM donations")
        all_donations = cursor.fetchall()
        return all_donations
    except mysql.connector.Error as err:
        print("Error fetching all donations:", err)
        return []




def add_donator(name, email, first_time_donating, gender):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO donators (name, email, first_time_donating, gender) VALUES (%s, %s, %s, %s)", (name, email, first_time_donating, gender))
        connection.commit()
    except mysql.connector.Error as err:
        print("Error: ", err)
    finally:
        cursor.close()
        connection.close()




def donated_people( email, amount_donated, category_name, user_email):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO the_donated_people ( email, amount_donated, category_name, user_email) VALUES ( %s, %s, %s, %s)", (email, amount_donated, category_name, user_email))
    connection.commit()
    cursor.close()
    connection.close()



def get_donated_persons():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT email, amount_donated, category_name, user_email FROM the_donated_people")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result



def get_request_by_id(request_id):
    try:
        # Establish a MySQL database connection
        # connection = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     password='',
        #     database='crowd_funding'
        # )
        connection = mysql.connector.connect(**config)


        cursor = connection.cursor(dictionary=True)

        # Query to retrieve the request and user_email from the database
        query = "SELECT * FROM pend_requests WHERE id = %s"
        cursor.execute(query, (request_id,))
        
        # Fetch the result (assuming 'user_email' is a column in your 'requests' table)
        row = cursor.fetchone()

        if row:
            request = row
            user_email = row['user_email']  # Replace with the actual column name in your table
            return request, user_email
        else:
            return None, None

    except mysql.connector.Error as e:
        # Handle any database errors here
        print(f"Error: {e}")
        return None, None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def update_request_approval(request_id, approved):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # SQL UPDATE statement
        update_query = """
        UPDATE pend_requests
        SET approved = %s
        WHERE id = %s
        """

        # Values to update the approval status
        values = (approved, request_id)

        cursor.execute(update_query, values)
        connection.commit()
        
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        return False
    
    

    
def insert_needed_amount(category_id, amount_needed):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "INSERT INTO donations_balance (category_id, amount_remaining) VALUES (%s, %s)"
    cursor.execute(query, (category_id, amount_needed))
    
    connection.commit()
    cursor.close()
    connection.close()
    



def update_amount(id, donated_amount):
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Decrease the amount remaining by the donated amount
        query = """
            UPDATE donations_balance
            SET amount_remaining = amount_remaining - %s
            WHERE id = %s AND amount_remaining >= %s
        """
        cursor.execute(query, (donated_amount, id, donated_amount))
        
        connection.commit()
        cursor.close()
        connection.close()




def update_balance_in_categories(category_id, new_balance):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = """
    UPDATE categories
    SET balance = %s
    WHERE id = %s
    """
    cursor.execute(query, (new_balance, category_id))
    
    connection.commit()
    cursor.close()
    connection.close()