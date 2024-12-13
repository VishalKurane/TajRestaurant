import azure.functions as func
import logging
import pyodbc
import os
import json
import jwt
from datetime import datetime, timedelta, timezone


dbUrl = os.environ['DBConnectionString']

# Secret key for JWT encoding
SECRET_KEY = os.environ['JWT_SECRET_KEY']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing a Admin login request.")

    try:
        # Parse the request JSON data
        login_data = req.get_json()
        email = login_data.get("email")
        password_hash = login_data.get("password_hash")

        if not all([email, password_hash]):
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: 'Email' or 'Password'"}),
                status_code=400,
                mimetype="application/json"
            )

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute('SELECT password_hash FROM AdminTable WHERE email = ?', (email,))
        row = cursor.fetchone()

        if row:
            # User exists, check password
            stored_password_hash = row[0]
            if stored_password_hash == password_hash:
                # # Password matches
                # logging.info(f"User {email} authenticated successfully.")
                # response_message = "Authentication successful."
                # response_status = 200
                
                # Generate JWT token
                # Token expiration set to 1 hour in UTC
                expiration = datetime.now(timezone.utc) + timedelta(hours=1)
                token = jwt.encode(
                    {
                        "sub": email,
                        "email": email,
                        "exp": expiration
                    },
                    SECRET_KEY,
                    algorithm="HS256"
                )

                # On successful authentication, return a JSON response with the JWT
                response_data = {
                    "message": "Authentication successful",
                    "access_token": token
                }
                response_status = 200
                logging.info(f"Authentication successful for Admin: {email}")
                
            else:
                # Password does not match
                logging.warning(f"Admin {email} provided an incorrect password.")
                response_data = {"error": "Incorrect password"}
                response_status = 401
        else:
            # User does not exist
            logging.warning(f"Admin {email} not found in the database.")
            response_data = {"error": "Admin not found"}
            response_status = 404

        # Close database connections
        cursor.close()
        conn.close()

        # Return JSON response
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=response_status,
            mimetype="application/json"
        )
    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(
            json.dumps({"error": f"An error occurred while processing your request: {e}"}),
            status_code=500,
            mimetype="application/json"
        )
