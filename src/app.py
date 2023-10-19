from flask import Flask, jsonify, Blueprint, session, request
import os
import mysql.connector
from database import config
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import random
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from utilities import send_otp, approved_mail, send_mail, approved_mail_donators, received, received_admin
from models import add_user, get_user_by_id, get_user, add_category, add_request, get_user_requests, get_all_requests, is_user_admin, update_request_approval, get_donated_persons, get_request_by_id, query_cat_id, donated_people, requests_for_donators, set_request_status, get_all_approved_requests, get_minimum_amount,update_amount, insert_needed_amount, update_balance_in_categories
from decimal import Decimal


def insert_needed_amount(category_id, amount_needed):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    query = "INSERT INTO donations_balance (category_id, amount_remaining) VALUES (%s, %s)"
    cursor.execute(query, (category_id, amount_needed))
    
    connection.commit()
    cursor.close()
    connection.close()
    


app = Flask(__name__)

bcrypt = Bcrypt(app)
jwt = JWTManager()
auth = Blueprint("auth", __name__)

app.config.from_pyfile('config.py')

mail = Mail(app)

# SECRET_KEY = 'language007'

def send_otp(email, otp):
    msg = Message('Verification Token', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Your verification token is {otp}'
    print('otp :', otp)
    mail.send(msg)



def approved_mail(email):
    msg = Message(' Congratulations your request has been approved, you can now receive donations', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Congratulations your request has been approved, you can now receive donations 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    mail.send(msg)

def send_mail(email):
    msg = Message('Verification Email', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You just successfully registered on speedyhelp as a donator. Thank you 🎉🎉🎉🎉🥳🥳🎆🎆🥂🥂🎇🎇'
    mail.send(msg)

def approved_mail_donators(email):
    msg = Message('Thank you for your donations ❤❤❤', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'Thank you for your donations on speedyhelp ❤❤❤'
    mail.send(msg)


def received(email):
    msg = Message('You have just received an anonymous donation', sender='Anonymous@gmail.com', recipients=[email])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    mail.send(msg)

def received_admin(username):
    msg = Message(f'{username} received an anonymous donation', sender='Anonymous@gmail.com', recipients=['admin@gmail.com'])
    msg.body = f'You have just received an anonymous donation on speedyhelp'
    mail.send(msg)

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.secret_key = 'language007'        
    jwt.init_app(app)
    app.register_blueprint(auth, url_prefix='/auth/v1')
    mail.init_app(app)
    return app


# mail = Mail(app)



def email_exists(email):
    user = get_user(email)  
    return user is not None


@auth.route('/register', methods=[ 'POST'])
def register():
    data = request.get_json()
    if request.method == 'POST':
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        
        # Check if email is unique
        if email_exists(email):
            return jsonify({
                'message': 'Email already exists.', 
                "status": 400
            })

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        otp = random.randint(1000, 9999)
        session['otp'] = otp
        send_otp(email, otp)
        # Change to true if creating an admin
        add_user(first_name, last_name, email, hashed_password, False)
        return jsonify({
            'message': 'Please enter your OTP',  
            'otp': otp,  
            "status": 200
        })

        


@auth.route('/token/<email>', methods=['GET', 'POST'])
def token(email):
    data = request.get_json()
    if request.method == 'POST':
        token = data.get('otp')
        
        
        stored_otp = session.get('otp', None)
        if token != str(stored_otp):
            print('token:', token)
            print('otp:', stored_otp)
            return jsonify({'message': 'Invalid Token', 'status': 400})
        else:
            return jsonify({'message': 'You have been verified', 'status': 200})



@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Missing JSON in request', 'status': 400}), 400
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password', 'status': 400}), 400

    # Assuming the function get_user_by_email() is defined to fetch user details using email
    user = get_user(email)
    # print(user["email"])
    
    if user and bcrypt.check_password_hash(user.password, password):
        # Generate the JWT token
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'status': 200
        }), 200
    print('Login successful')
    return jsonify({'message': 'Invalid email or password', 'status': 400}), 400


# @auth.route('/admin', methods=['GET'])
# @jwt_required()
# def admin():
#     return jsonify({'message': 'You are an admin', 'status': 200}), 200



@auth.route('/category', methods=['GET', 'POST'])
@jwt_required()
def category():
    user_id = get_jwt_identity()
    
    categories = ['Animals', 'Education', 'Medical', 'Funeral', 'Events', 'Family', 'Faith', 'Travel', 'Monthly-Bills', 'Sports', 'Others', 'Emergencies']
    
    fund_for = ['Myself', 'Others']
    
    
    
    if request.method == 'GET':
        categories = ['Animals', 'Education', 'Medical', 'Funeral', 'Events', 'Family', 'Faith', 'Travel', 'Monthly-Bills', 'Sports', 'Others', 'Emergencies']
    
        fund_for = ['Myself', 'Others']
        return jsonify({'message': 'These are the categories', 'categories': categories, 'fund_for': fund_for, 'status': 200}), 200
    
    data = request.get_json()
    user_email = data.get('user_email', None)

    # Check if required fields are present
    for field in ['user_email','category_name', 'fundraising_for', 'amount', 'expiryDate', 'minimum_amount']:
        if not data.get(field):
            return jsonify({'message': f'Missing {field}', 'status': 400}), 400

    # Check for category and fundraising-for validity
    if data.get('category_name') not in categories:
        return jsonify({'message': 'Invalid category. Please choose a valid category.', 'status': 400}), 400

    if data.get('fundraising_for') not in fund_for:
        return jsonify({'message': 'Invalid fund-for option. Please choose a valid option.', 'status': 400}), 400
    
    
    # Further validation for other fields can be added here

    # Assuming the functions add_request and add_category handle their internal errors and return a boolean indicating success
    print(data['user_email'])
    
    if not add_request(  data['user_email'], data['category_name'], data['fundraising_for'], data['expiryDate'], data['amount'], data['description'], data['minimum_amount']):
        return jsonify({'message': 'Error adding request. Try again later.', 'status': 500}), 500
    
    add_category(user_id, data['category_name'], data['fundraising_for'], data['expiryDate'], data['amount'], data['description'], data['minimum_amount'], data['amount'])

        # return jsonify({'message': 'Error adding category. Try again later.', 'status': 500}), 500

    return jsonify({'message': 'Category added successfully', 'status': 200}), 200



# View_Requests routes (users)
@auth.route('/view_request', methods=['GET'])
@jwt_required()
def view_request():
    user_id = get_jwt_identity()
    # user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID not provided', 'status': 400}), 400

    user_requests = get_user_requests(user_id)
    return jsonify({'requests': user_requests, 'status': 200}), 200



# Login route
@auth.route("/logout", methods=['GET', 'POST'])
@jwt_required()
def logout():
    session.pop('user', None)
    return jsonify({'message': 'You have been logged out', 'status': 200}), 200




# Admin route
@auth.route('/see_requests', methods=['GET', 'POST'])
@jwt_required()  
def see_requests():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)  
    
    if not user or not user.email:
        return jsonify({'message': 'Error retrieving user details.', 'status': 500}), 500
    
    if not is_user_admin(user.email):
        return jsonify({'message': 'Access forbidden: You are not authorized to view this resource.', 'status': 403}), 403

    data = get_all_requests()

    return jsonify({'message': 'These are the users requests', 'requests': data, 'status': 200}), 200



@auth.route('/approve_request/<int:request_id>', methods=['POST'])
@jwt_required()
def approve_request(request_id):
    # Retrieve the request and user_email from the database using request_id
    request_details, user_email = get_request_by_id(request_id)

    # Check if the request exists
    if request_details:
        if not request_details.get('approved', False):
            # Update the request's approval status to True
            if update_request_approval(request_id, True):
                approved_mail(user_email)
                if not requests_for_donators(user_email, request_details['category_name'], request_details['amount'], request_details['description']):
                    return jsonify({'message': 'An error occurred while adding request', 'status': 500}), 500
                return jsonify({'message': 'Request approved successfully', 'status': 200,}), 200
            else:
                return jsonify({'message': 'An error occurred while approving requests', 'status': 500}), 500
        else:
            return jsonify({'message': 'Request already approved', 'status': 400}), 400
    else:
        return jsonify({'message': 'Request not found', 'status': 404}), 404
    





@auth.route('/see_approved_requests', methods=['GET'])
def see_approved_requests():
    approved_requests = get_all_approved_requests()
    return jsonify({
        'message': 'These are the approved requests', 
        'Requests': approved_requests, 
        'status': 200
    }), 200







from models import fetch_category_by_id

@auth.route('/start_donating/<int:id>', methods=['POST'])
def start_donating(id):
    json_data = request.get_json()
    balance_before = None
    # Ensure JSON data was provided
    if not json_data:
        return jsonify({'message': 'No JSON data provided', 'status': 400}), 400

    donor_email = json_data.get('email')
    donated_amount_data = json_data.get('amount_donated')
    category_name = json_data.get('category_name')
    user_email = json_data.get('user_email')
    # mininum_amount = json_data.get('minimum_amount')

    if not all([donor_email, donated_amount_data, category_name, user_email]):
        return jsonify({'message': 'Some required data is missing', 'status': 400}), 400

    donated_amount = float(donated_amount_data)

    cat = fetch_category_by_id(id)
    if not cat:
        return jsonify({'message': 'Category not found', 'status': 404}), 404
    balance = cat['balance']
    if donated_amount_data > balance:
        return jsonify({'message': 'You cannot donate more than the required amount', 'balance': balance}), 400

    minimun_donation = cat['minimum_amount']
    if donated_amount < minimun_donation:
        return jsonify({'message': 'You cannot donate less than the minimum amount', 
        'minimum_amount': minimun_donation}), 400

    new_balance = float(balance) - donated_amount
    update_balance_in_categories(id, new_balance)
    # save into database

    
    
    donated_people(donor_email, donated_amount, category_name, user_email)
    # requests_for_donators(user_email, category_name, user_request['amount'], user_request['description'])

    # new_balance = float(stored_balance) - donated_amount

    print(new_balance)
    approved_mail_donators(donor_email)
    received(user_email)
    received_admin(user_email)
    return jsonify({
        'message': 'You have successfully donated',
        'status': 200,
        'amount_donated': donated_amount,
        'category_name': category_name,
        'receiver email': user_email,
        'remaining_balance': new_balance,
        'sender': donor_email,
    }), 200




@auth.route('/see_donators', methods=['GET'])
@jwt_required()
def see_donators():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    data = get_donated_persons()
    print(data)
    if not user or not user_id:
        return jsonify({'message': 'Error retrieving user details.', 'status': 500}), 500
    
    if not is_user_admin(user.email):
        return jsonify({'message': 'Access forbidden: You are not authorized to view this resource.', 'status': 403}), 403

    print('oooooooooooo')
    print(data)
    return jsonify({'message': 'These are the donators', 'Donation_info': data ,'status': 200}), 200








if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)