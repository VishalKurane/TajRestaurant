import azure.functions as func
import logging
import os
import pyodbc
import json

dbUrl = os.environ['DBConnectionString']

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a request to get users.')

    try:

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT userid, full_name, email, phone, created_at FROM UserTable'
        )
        users = []
            
        for row in cursor.fetchall():
            user = {
                "userid": row.userid,
                "full_name": row.full_name,
                "email": row.email,
                "phone": row.phone,
                "created_at": row.created_at.strftime('%Y-%m-%d %H:%M')
            }
            users.append(user)


        # Close database connections
        cursor.close()
        conn.close()

        # Return the created user data
        logging.info(f"User list fetched successfully.")
        return func.HttpResponse(json.dumps(users), status_code=200, mimetype='application/json')
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    