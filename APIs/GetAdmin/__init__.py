import azure.functions as func
import logging
import os
import pyodbc

dbUrl = os.environ['DBConnectionString']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new user creation request.')

    try:
        # Parse the request JSON data
        new_user = req.get_json()
        full_name = new_user.get("full_name")
        email = new_user.get("email")
        phone = new_user.get("phone")
        password_hash = new_user.get("password_hash")
        
        if not all([full_name, email, phone, password_hash]):
            return func.HttpResponse(
                "Missing required fields in request: 'Name', 'Email', 'Phone' or 'Password'",
                status_code=400
            )

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO UserTable (full_name, email, phone, password_hash) VALUES (?, ?, ?, ?)',
            (full_name, email, phone, password_hash)
        )
        conn.commit()

        # Close database connections
        cursor.close()
        conn.close()

        # Return the Admin data
        logging.info(f"User {full_name} created successfully.")
        return func.HttpResponse(
            f"User {full_name} created successfully.",
            status_code=201
        )
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    