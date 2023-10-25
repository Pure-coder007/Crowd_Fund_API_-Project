import mysql.connector
from mysql.connector import Error



# config = {
#     'user': 'project_101',
#     'password': 'language007',
#     'host': 'db4free.net',
#     'port': '3306',
#     'database': 'ap_project'
# }


config = {
    'user' : 'root',
    'password' : 'language007',
    'host' : 'localhost',
    'port' : '3306',
    'database' : 'crowd_fund_api'
}



def setup_database():
    config['database'] = None
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()



# User Table
    cursor.execute("""
    CREATE TABLE user(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,  
    password VARCHAR(255) NOT NULL,      
    is_admin BOOLEAN DEFAULT FALSE,      
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  
);

""")



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    fundraising_for VARCHAR(255) NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    description TEXT,
    expiry_date DATE,
    minimum_amount DECIMAL(20, 2),
    user_email VARCHAR(100),
    request_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    request_id INT NOT NULL
);

    """)



    cursor.execute("""
    CREATE TABLE donators(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_time_donating BOOLEAN NOT NULL,
    gender VARCHAR(10) NOT NULL,
);

""")
    



    cursor.execute("""
    CREATE TABLE donations_info(
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount_donated DECIMAL(10, 2),
    donator_name VARCHAR(255),
    required_amount DECIMAL(10, 2),
    email VARCHAR(255),
    cat_id INT NOT NULL
);
                  
""")



    cursor.execute("""    
    CREATE TABLE pend_requests (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    fundraising_for VARCHAR(255) NOT NULL,
    expiry_date DATE,
    amount DECIMAL(20,2) NOT NULL,
    description TEXT,
    approved TINYINT(4) DEFAULT 0
                   
);
""")
    

    cursor.execute("""
    CREATE TABLE approved_requests (
    id INT(11) NOT NULL PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    fundraising_for VARCHAR(255) NOT NULL,
    expiry_date DATE NOT NULL,
    amount DECIMAL(20,2) NOT NULL
);
""")
    
    cursor.execute("""
    CREATE TABLE donated_people (
    id INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    amount_donated DECIMAL(20,2) NOT NULL,
    category_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL
);
""")

    cursor.execute("""
    CREATE TABLE donator_view (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    category_name VARCHAR(255),
    amount DECIMAL(10,2),
    description TEXT
);
""")



    connection.commit()
    cursor.close()
    connection.close()
  
    
# try:
#     # Setup the connection
#     connection = mysql.connector.connect(
#         host='db4free.net',
#         user='project_101',
#         password='language007',
#         database='ap_project'
#     )

#     if connection.is_connected():
#         db_info = connection.get_server_info()
#         print(f"Connected to MySQL server version {db_info}")
#         cursor = connection.cursor()
#         cursor.execute("SELECT DATABASE();")
#         db_name = cursor.fetchone()[0]
#         print(f"You're connected to the database: {db_name}")

# except Error as e:
#     print(f"Error: {e}")

# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection closed.")
    
    
    
    if __name__ == "__main__":
        setup_database()