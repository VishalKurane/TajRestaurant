from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, send_from_directory
import logging
import jwt
import requests
import os
import pytz
from datetime import datetime

# Initialize Flask
app = Flask(__name__)

# Custom formatter to get the timestamp in IST
class ISTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # Convert the timestamp to IST (UTC+5:30)
        tz = pytz.timezone('Asia/Kolkata')
        created_time = datetime.fromtimestamp(record.created, tz)
        if datefmt:
            return created_time.strftime(datefmt)
        else:
            return created_time.strftime('%Y-%m-%d %H:%M:%S')

# Clear the existing handlers to avoid duplicate logs
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Logging setup
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Use custom IST formatter
formatter = ISTFormatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel(logging.INFO)  # Set the desired logging level

#################################################################################################

# JWT configuration
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def validate_token(token):
    AZ_FUNCTION_VALIDATE_TOKEN = os.getenv('AZ_FUNCTION_VALIDATE_TOKEN')

    response = requests.post(AZ_FUNCTION_VALIDATE_TOKEN, json={"token": token})
    return response

def token_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("access_token")
        if not token:
            # return jsonify({"message": "Token is missing!"}), 401
            logging.info(f"Trying to access 'Home Service' but Token is missing!")
            return redirect('/auth/login')

        response = validate_token(token)
        if response.status_code != 200:
            # return jsonify({"message": "Invalid token!"}), 401
            logging.info(f"Trying to access 'Home Service' but Token is Invalid!")
            return redirect('/auth/login')

        return func(*args, **kwargs)
    return wrapper

#################################################################################################


@app.route('/', methods=['GET'])
@token_required
def home():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /home endpoint by user: {current_user}")
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Error accessing Home page: {e}")
        return redirect('/auth/login')


@app.route('/about', methods=['GET'], endpoint='about_page')
@token_required
def about():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /about endpoint by user: {current_user}")
        return render_template('about.html')
    except Exception as e:
        logging.error(f"Error accessing About page: {e}")
        return redirect('/auth/login')
  

@app.route('/menu', methods=['GET'], endpoint='menu_page')
@token_required
def menu():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /menu endpoint by user: {current_user}")
        return redirect('/menu')
    except Exception as e:
        logging.error(f"Error accessing Menu page: {e}")
        return redirect('/auth/login')

@app.route('/config')
# @token_required
def get_config():
    AZ_FUNCTION_GET_MENU = os.getenv("AZ_FUNCTION_GET_MENU")
    return {
        "AZ_FUNCTION_GET_MENU": AZ_FUNCTION_GET_MENU
    }

@app.route('/reservation', methods=['GET', 'POST'], endpoint='reservation_page')
@token_required
def reservation():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /reservation endpoint by user: {current_user}")
        return redirect('/reservation')
    except Exception as e:
        logging.error(f"Error accessing Reservation page: {e}")
        return redirect('/auth/login')
    

@app.route('/contact', methods=['GET'], endpoint='contact_page')
@token_required
def contact():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /contact endpoint by user: {current_user}")
        return render_template('contact.html')
    except Exception as e:
        logging.error(f"Error accessing Contact page: {e}")
        return redirect('/auth/login')
  

@app.route('/logout')
def logout():
    response = make_response(redirect('/auth/login'))
    response.set_cookie('jwt_token', '', expires=0, path='/') 
    
    # Add headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run()