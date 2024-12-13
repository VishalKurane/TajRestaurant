import azure.functions as func
import logging
import os
import pyodbc
import json

dbUrl = os.environ['DBConnectionString']

CATEGORY_ORDER = [
    "BREAKFAST",
    "VEG",
    "NON-VEG",
    "ROTI, NAAN & RICE",
    "DESSERTS",
    "HOT & COLD SIPS"
]

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new request to get Menus.')

    try:
        
        # Query to fetch menu data
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT menu_category, menu_name, menu_description, menu_price, image_url FROM MenuTable'
        )
        rows = cursor.fetchall()

        # Organize data into categories
        menu = {}
        for menu_category, menu_name, menu_description, menu_price, image_url in rows:
            if menu_category not in menu:
                menu[menu_category] = []
            menu[menu_category].append({
                'name': menu_name,
                'description': menu_description,
                'price': float(menu_price),
                'image_url': image_url

            })

        # Format data for response
        menu_list = [
            {'Category': category, 'Menus': menu.get(category, [])} 
            for category in CATEGORY_ORDER
        ]

        # Close database connections
        cursor.close()
        conn.close()

        # Return the created user data
        logging.info(f"Get /GetMenu executed successfully.")
        return func.HttpResponse(
            json.dumps(menu_list),  
            status_code=200,        
            mimetype='application/json'
        )
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    