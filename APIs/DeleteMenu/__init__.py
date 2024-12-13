import azure.functions as func
import logging
import os
import pyodbc

dbUrl = os.environ['DBConnectionString']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new request.')

    try:
        # Parse the request JSON data
        menu = req.get_json()
        category = menu.get("category")
        menuName = menu.get("menuName")
        
        
        if not all([category, menuName]):
            return func.HttpResponse(
                "Missing required fields in request: 'Category' or 'Menu Name'",
                status_code=400
            )

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'DELETE FROM MenuTable WHERE menu_category = ? AND menu_name = ?',
            (category, menuName)
        )
        conn.commit()

        # Close database connections
        cursor.close()
        conn.close()

        # Return the created user data
        logging.info(f"Menu Deleted Successfully.")
        return func.HttpResponse(
            f"Menu Deleted Successfully.",
            status_code=201
        )
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    