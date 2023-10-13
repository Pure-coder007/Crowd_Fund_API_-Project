from flask import Flask, jsonify, Blueprint, session, request
import os
# from auth import auth
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import random
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from utilities import send_otp, approved_mail, send_mail, approved_mail_donators, received, received_admin
from models import add_user, get_user_by_id, get_user, add_category, add_request



app = Flask(__name__)
auth = Blueprint("auth", __name__)

bcrypt = Bcrypt(app)
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    app.config['SECRET_KEY'] = 'IHDJHDKJHJDHM'
    app.config['JWT_SECRET_KEY']='language007'  
    
    jwt.init_app(app)


    # if test_config is None:
    #     app.config.from_mapping(
    #         SECRET_KEY=os.environ.get("kingsley")
    #         )
    # else:
    #     app.config.from_mapping(test_config)

    app.register_blueprint(auth, url_prefix='/auth/v1')

    return app

# app.config.from_pyfile('config.py')
mail = Mail(app)




@auth.route('/register', methods=[ 'POST'])
def register():
    data = request.get_json()
    if request.method == 'POST':
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        password = data['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        
        otp = random.randint(1000, 9999)
        session['otp'] = otp
        # send_otp(email, otp)
        # Change to true if creating an admin
        add_user(first_name, last_name, email, hashed_password, False)
        # send_otp(email)
        return jsonify({
            'message': 'Please enter your OTP',  'otp': otp,  "status": 200})
        


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
    # return render_template('token.html')



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



@auth.route('/category', methods=['POST'])
@jwt_required()
def category():
    data = request.get_json()
    user_id = get_jwt_identity()
    print(data)
    categories = ['Animals', 'Education', 'Medical', 'Funeral', 'Events', 'Family', 'Faith', 'Travel', 'Monthly-Bills', 'Sports', 'Others', 'Emergencies']
    fund_for = ['Myself', 'Others']
    user_email = data.get('user_email', None)
    # user_email = data.get('user_email', None)
    # if not user_email:
    #     return jsonify({'message': 'user_email is required', 'status': 400}), 400

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
    
    if not add_request(  data['user_email'], data['category_name'], data['fundraising_for'], data['expiryDate'], data['amount'], data['description']):
        return jsonify({'message': 'Error adding request. Try again later.', 'status': 500}), 500
    
    add_category(user_id,data['category_name'], data['fundraising_for'], data['expiryDate'], data['amount'], data['description'], data['minimum_amount'])
        # return jsonify({'message': 'Error adding category. Try again later.', 'status': 500}), 500

    return jsonify({'message': 'Category added successfully', 'status': 200}), 200





if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)