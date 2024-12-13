from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
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
            return redirect('/auth')

        response = validate_token(token)
        if response.status_code != 200:
            # return jsonify({"message": "Invalid token!"}), 401
            logging.info(f"Trying to access 'Home Service' but Token is Invalid!")
            return redirect('/auth')

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
        return redirect('/auth')


@app.route('/user', methods=['GET'], endpoint='user')
@token_required
def user():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /user endpoint by user: {current_user}")
        return render_template('user.html')
    except Exception as e:
        logging.error(f"Error accessing About page: {e}")
        return redirect('/auth')

@app.route('/adminuser', methods=['GET'], endpoint='adminuser')
@token_required
def contact():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /adminuser endpoint by user: {current_user}")
        return render_template('adminuser.html')
    except Exception as e:
        logging.error(f"Error accessing Contact page: {e}")
        return redirect('/auth')
    


@app.route('/menu', methods=['GET'], endpoint='menu')
@token_required
def menu():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /menu endpoint by user: {current_user}")
        return redirect('/menu')
    except Exception as e:
        logging.error(f"Error accessing Menu page: {e}")
        return redirect('/auth')
    

@app.route('/reservation', methods=['GET', 'POST'], endpoint='reservation')
@token_required
def reservation():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /reservation endpoint by user: {current_user}")
        return redirect('/reservation')
    except Exception as e:
        logging.error(f"Error accessing Reservation page: {e}")
        return redirect('/auth')
    

@app.route('/removeuser', methods=['GET', 'POST'], endpoint='removeuser')
@token_required
def removeuser():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /removeuser endpoint by user: {current_user}")


        userid = request.form['userid']
        params = {
                    "userid": userid
                }

        AZ_FUNCTION_REMOVE_USER = os.getenv('AZ_FUNCTION_REMOVE_USER')

        response = requests.delete(AZ_FUNCTION_REMOVE_USER, json=params)
        response.raise_for_status()
        logging.info(f"Status Code for AZ_FUNCTION_REMOVE_USER: {response.status_code}")
        logging.info(f"Response Message for AZ_FUNCTION_REMOVE_USER: {response.text}")
        logging.info(f"User with ID-{userid} removed from Database")


        return redirect(url_for('user'))
    except Exception as e:
        logging.error(f"Error Adding the Menu: {e}")
        return redirect('/auth')
    

# =========================================
@app.route('/config')
# @token_required
def get_config():
    AZ_FUNCTION_GET_MENU = os.getenv("AZ_FUNCTION_GET_MENU")
    AZ_FUNCTION_GET_BOOKING = os.getenv("AZ_FUNCTION_GET_BOOKING")
    AZ_FUNCTION_DELETE_RESERVATION = os.getenv("AZ_FUNCTION_DELETE_RESERVATION")
    return {
        "AZ_FUNCTION_GET_MENU": AZ_FUNCTION_GET_MENU,
        "AZ_FUNCTION_GET_BOOKING": AZ_FUNCTION_GET_BOOKING,
        "AZ_FUNCTION_DELETE_RESERVATION": AZ_FUNCTION_DELETE_RESERVATION
    }

@app.route('/addmenu', methods=['POST'], endpoint='addmenu')
@token_required
def addmenu():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /addmenu emdpoint by user: {current_user}")

        category = request.form['category']
        menuName = request.form['menuName']
        menuDescription = request.form['menuDescription']
        menuPrice = request.form['menuPrice']
        imageUrl = request.form['imageUrl']

        if category == "BREAKFAST" :
            menuCategory = "BREAKFAST"

        elif category == "VEG" :
            menuCategory = "VEG"

        elif category == "NON-VEG" :
            menuCategory = "NON-VEG"

        elif category == "ROTI_NAAN_RICE" :
            menuCategory = "ROTI, NAAN & RICE"

        elif category == "DESSERTS" :
            menuCategory = "DESSERTS"

        elif category == "HOT_COLD_SIPS" :
            menuCategory = "HOT & COLD SIPS"

        New_menu = {
            "category": menuCategory,
            "menuName": menuName,
            "menuDescription": menuDescription,
            "menuPrice": menuPrice,
            "imageUrl": imageUrl
        }

        AZ_FUNCTION_ADD_MENU = os.getenv('AZ_FUNCTION_ADD_MENU')

        response = requests.post(AZ_FUNCTION_ADD_MENU, json=New_menu)
        response.raise_for_status()
        logging.info(f"Status Code for AZ_FUNCTION_ADD_MENU: {response.status_code}")
        logging.info(f"Response Message for AZ_FUNCTION_ADD_MENU: {response.text}")
        logging.info(f"Successfully '{menuName}' menu added in the MenuCard")

        return redirect('/menu')
    except Exception as e:
        logging.error(f"Error Adding the Menu: {e}")
        return redirect('/menu')


@app.route('/removemenu', methods=['POST'], endpoint='removemenu')
@token_required
def removemenu():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        logging.info(f"Accessed /removemenu endpoint by user: {current_user}")

        category = request.form['category']
        menuName = request.form['menuName']

        if category == "BREAKFAST" :
            menuCategory = "BREAKFAST"

        elif category == "VEG" :
            menuCategory = "VEG"

        elif category == "NON-VEG" :
            menuCategory = "NON-VEG"

        elif category == "ROTI_NAAN_RICE" :
            menuCategory = "ROTI, NAAN & RICE"

        elif category == "DESSERTS" :
            menuCategory = "DESSERTS"

        elif category == "HOT_COLD_SIPS" :
            menuCategory = "HOT & COLD SIPS"

        menu = {
            "category": menuCategory,
            "menuName": menuName
        }

        AZ_FUNCTION_REMOVE_MENU = os.getenv('AZ_FUNCTION_REMOVE_MENU')

        response = requests.post(AZ_FUNCTION_REMOVE_MENU, json=menu)
        response.raise_for_status()
        logging.info(f"Status Code for AZ_FUNCTION_REMOVE_MENU: {response.status_code}")
        logging.info(f"Response Message for AZ_FUNCTION_REMOVE_MENU: {response.text}")
        logging.info(f"Successfully '{menuName}' menu removed from the MenuCard")

        return redirect('/menu')
    except Exception as e:
        logging.error(f"Error Adding the Menu: {e}")
        return redirect('/menu')


# =========================================

@app.route('/logout')
def logout():
    response = make_response(redirect('/auth'))
    response.set_cookie('jwt_token', '', expires=0, path='/') 
    
    # Add headers to prevent caching
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run()