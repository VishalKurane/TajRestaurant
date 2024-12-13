from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import logging
import jwt
import requests
import json
import os
import pytz
from datetime import datetime

from azure.servicebus import ServiceBusClient, ServiceBusMessage


SERVICE_BUS_CONNECTION_STRING = os.getenv('SERVICE_BUS_CONNECTION_STRING')
QUEUE_NAME = os.getenv('QUEUE_NAME')


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
            logging.info(f"Trying to access 'Reservation Service' but Token is missing!")
            return redirect('/auth/login')

        response = validate_token(token)
        if response.status_code != 200:
            # return jsonify({"message": "Invalid token!"}), 401
            logging.info(f"Trying to access 'Reservation Service' but Token is Invalid!")
            return redirect('/auth/login')

        return func(*args, **kwargs)
    return wrapper

#################################################################################################

@app.route('/', methods=['GET', 'POST'], endpoint='reservation')
@token_required
def reservation():
    try:
        decoded_token = jwt.decode(request.cookies.get("access_token"), SECRET_KEY, algorithms=["HS256"])
        current_user = decoded_token.get("email", "Unknown User")
        
        if request.method == 'POST':
            Guest_name = request.form.get('name')
            Guest_email = request.form.get('email')
            Guest_phone = request.form.get('phone')
            Guest_check_in = request.form.get('checkin')
            Guest_chcek_in_time = request.form.get('time')
            No_of_guests = request.form['countofguest']

            booking_data = {
                "user": current_user,
                "Guest_name": Guest_name,
                "Guest_email": Guest_email,
                "Guest_phone": Guest_phone,
                "check_in_date": Guest_check_in,
                "check_in_time": Guest_chcek_in_time,
                "No_of_guests": No_of_guests,
            }

            # Push booking_data to Azure Service Bus queue
            try:
                servicebus_client = ServiceBusClient.from_connection_string(conn_str=SERVICE_BUS_CONNECTION_STRING)
                with servicebus_client:
                    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
                    with sender:
                        message = ServiceBusMessage(json.dumps(booking_data))
                        sender.send_messages(message)
                        logging.info("Reservation Data Message sent to Azure Service Bus successfully.")
            except Exception as servicebus_error:
                logging.error(f"Failed to send message to Azure Service Bus: {servicebus_error}")
                return "Error processing reservation. Please try again later.", 500

            return render_template('success.html')
        
        logging.info(f"Accessed /reservation endpoint by user: {current_user}")
        return render_template('/reservation.html')
    except Exception as e:
        logging.error(f"Error accessing reservation page: {e}")
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()