import azure.functions as func
import logging
import os
import pyodbc

dbUrl = os.environ['DBConnectionString']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new request to add menu.')

    try:
        # Parse the request JSON data
        new_menu = req.get_json()
        category = new_menu.get("category")
        menuName = new_menu.get("menuName")
        menuDescription = new_menu.get("menuDescription")
        menuPrice = new_menu.get("menuPrice")
        imageUrl = new_menu.get("imageUrl")
        
        if not all([category, menuName, menuPrice]):
            return func.HttpResponse(
                "Missing required fields in request: 'Category', 'Menu Name'or 'Menu Price'",
                status_code=400
            )

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO MenuTable (menu_category, menu_name, menu_description, menu_price, image_url) VALUES (?, ?, ?, ?, ?)',
            (category, menuName, menuDescription, menuPrice, imageUrl)
        )
        conn.commit()

        # Close database connections
        cursor.close()
        conn.close()

        # Return the created user data
        logging.info(f"{menuName}Menu Added Successfully.")
        return func.HttpResponse(
            f"Menu Added Successfully.",
            status_code=201
        )
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    