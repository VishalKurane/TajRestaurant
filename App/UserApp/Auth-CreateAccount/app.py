from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import requests
import logging
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

@app.route('/', methods=['GET', 'POST'])
def CreateAccount():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        # Prepare JSON data to send to Azure Function
        new_user = {
            "full_name": name,
            "email": email,
            "phone": phone,
            "password_hash": password
        }

        # Send POST request to Azure Function
        AZ_FUNCTION_ADD_USER = os.getenv('AZ_FUNCTION_ADD_USER')
        
        try:
            response = requests.post(AZ_FUNCTION_ADD_USER, json=new_user)
            response.raise_for_status()

            # Check the Azure Function response
            logging.info(f"Status Code for AZ_FUNCTION_ADD_USER: {response.status_code}")
            logging.info(f"Response Message for AZ_FUNCTION_ADD_USER: {response.text}")
            if response.status_code <= 201:
                logging.info(f"Account created successfully for '{name}' through API - AZ_FUNCTION_ADD_USER.")
                return redirect('/auth/login')
            else:
                logging.error(f"Failed to create account: {response.text}")
                return render_template('CreateAccount.html', error=f"Failed to create account: {response.text}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e}")
            return render_template('CreateAccount.html', error=f"Error connecting to the server: {e}")

    
    # Render the account creation form on GET request
    return render_template('CreateAccount.html')


if __name__ == '__main__':
    app.run()