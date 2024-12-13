import azure.functions as func
import logging
import os
import pyodbc
import json
from datetime import datetime


dbUrl = os.environ['DBConnectionString']

def fetch_reservations():
    try:
        # Query to fetch data
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT reservation_id, user_email, guest_name, guest_email, guest_phone, checkin_date, checkin_time, no_of_guest FROM ReservationTable'
        )

        # Fetch all rows and convert to a list of dictionaries
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        reservations = [dict(zip(columns, row)) for row in rows]

    
        # Close database connections
        cursor.close()
        conn.close()

        return reservations

    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a request to get the booking data.')

    try:
        # Fetch reservations from the database
        reservations = fetch_reservations()

        # Parse and sort reservations by checkin_date and checkin_time
        for record in reservations:
            checkin_datetime = datetime.strptime(
                f"{record['checkin_date']} {record['checkin_time']}", "%m/%d/%Y %I:%M%p"
            )
            record["checkin_datetime"] = checkin_datetime

        sorted_reservations = sorted(reservations, key=lambda x: x["checkin_datetime"])

        # Remove temporary sorting field before response
        for record in sorted_reservations:
            del record["checkin_datetime"]

        # Convert to JSON and return response
        response_body = json.dumps(sorted_reservations, indent=4)
        return func.HttpResponse(response_body, mimetype="application/json", status_code=200)
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    