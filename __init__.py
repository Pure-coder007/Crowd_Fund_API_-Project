from flask import Flask, jsonify
import os
from src.app import auth

# def create_app(test_config=None):
#     app = Flask(__name__,instance_relative_config=True)

#     app.config['SECRET_KEY'] = 'IHDJHDKJHJDHM'


#     # if test_config is None:
#     #     app.config.from_mapping(
#     #         SECRET_KEY=os.environ.get("kingsley")
#     #         )
#     # else:
#     #     app.config.from_mapping(test_config)

#     app.register_blueprint(auth, url_prefix='/auth/v1')

#     # @app.route('/hello')
#     # def sayHello():
#     #     return jsonify({'message': 'Hello kaycee!'}) 
     
#     return app

from src.app import *
