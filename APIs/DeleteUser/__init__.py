import azure.functions as func
import logging
import os
import pyodbc

dbUrl = os.environ['DBConnectionString']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing DeleteReservation request.")

    try:
        # Get the userid from the query parameters or request body
        userid = req.params.get('userid')
        if not userid:
            # Try to get the userid from the request body if not found in parameters
            req_body = req.get_json()
            userid = req_body.get('userid')
        
        # If userid is still not provided, return a bad request response
        if not userid:
            return func.HttpResponse(
                "Please provide the 'userid' parameter.",
                status_code=400
            )

        # Establish SQL connection
        with pyodbc.connect(dbUrl) as conn:
            cursor = conn.cursor()

            # SQL query to delete the user by userid
            cursor.execute("DELETE FROM UserTable WHERE userid = ?", userid)
            conn.commit()  # Commit the transaction

            # Check if the user was deleted
            if cursor.rowcount > 0:
                return func.HttpResponse(
                    f"User with userid {userid} successfully deleted.",
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    f"User with userid {userid} not found.",
                    status_code=404
                )

    except Exception as e:
        # Log the exception and return error response
        print(f"Error occurred: {str(e)}")
        return func.HttpResponse(
            f"An error occurred: {str(e)}",
            status_code=500
        )