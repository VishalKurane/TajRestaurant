import azure.functions as func
import logging
import os
import json
import pyodbc

dbUrl = os.environ['DBConnectionString']

async def main(msg: func.ServiceBusMessage):
    logging.info('Function triggered to process a message: %s', msg.get_body().decode('utf-8'))

    try:
        # Get the JSON payload from the message
        message_body = msg.get_body().decode('utf-8')
        data = json.loads(message_body)

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()

        # Insert data into the database
        insert_query = """
        INSERT INTO ReservationTable (user_email, guest_name, guest_email, guest_phone, checkin_date, checkin_time, no_of_guest)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(insert_query, 
                       data['user'], 
                       data['Guest_name'], 
                       data['Guest_email'], 
                       data['Guest_phone'], 
                       data['check_in_date'], 
                       data['check_in_time'], 
                       data['No_of_guests'])
        
        conn.commit()

        # Close database connections
        cursor.close()
        conn.close()

        # Return the created user data
        logging.info("Message processed and saved to database.")
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    