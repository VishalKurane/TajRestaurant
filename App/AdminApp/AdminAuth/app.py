from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import requests
import logging
import jwt
import os
import pytz
from datetime import datetime

# Initialize Flask and Blueprint
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
AZ_FUNCTION_ADMIN_LOGIN = os.getenv('AZ_FUNCTION_ADMIN_LOGIN')
AZ_FUNCTION_VALIDATE_TOKEN = os.getenv('AZ_FUNCTION_VALIDATE_TOKEN')

#################################################################################################

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        login_data = {
            "email": email,
            "password_hash": password
        }

        # Send POST request to Azure Function
        try:
            response = requests.post(AZ_FUNCTION_ADMIN_LOGIN, json=login_data)
            
            # Log status code and response content for debugging
            logging.info(f"Status Code for AZ_FUNCTION_ADMIN_LOGIN: {response.status_code}")
            # logging.info(f"Response Message for AZ_FUNCTION_ADMIN_LOGIN: {response.text}")

            if response.status_code == 200:
                logging.info(f"Admin '{email}' authenticated successfully.")
                data = response.json()
                if data.get("message") == "Authentication successful":
                    token = data.get("access_token")

                    # Set the token as a cookie
                    resp = make_response(redirect('/'))
                    resp.set_cookie("access_token", token)
                    return resp

            
            elif response.status_code == 401:
                logging.info(f"'{email}' - Invalid email or password")
                return render_template('loginPage.html', error="Invalid email or password.")
            
            else:
                logging.info(f"'{email}' - Authentication failed")
                return render_template('loginPage.html', error="Authentication failed.")

        except requests.RequestException as e:
            logging.error(f"Error connecting to Auth service: {e}")
            return render_template('loginPage.html', error="Service unavailable. Please try again later.")

    try:
        token = request.cookies.get("access_token")
        response = requests.post(AZ_FUNCTION_VALIDATE_TOKEN, json={"token": token})
        if response.status_code == 200:
            decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
            current_user = decoded_token.get("email", "Unknown User")
            logging.info(f"Accessed / endpoint by user: {current_user}")
            return redirect('/')

        else:
            return render_template('loginPage.html')
    
    except:
        # Render login page on GET request
        return render_template('loginPage.html')


if __name__ == '__main__':
    app.run()