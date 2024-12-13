import azure.functions as func
import logging
import os
import pyodbc

dbUrl = os.environ['DBConnectionString']


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing DeleteReservation request.")

    # Fetch reservation_id from the route
    reservation_id = req.route_params.get("reservation_id")
    if not reservation_id:
        return func.HttpResponse(
            "Reservation ID is required.",
            status_code=400,
        )
    
    try:

        # Connect to the database
        conn = pyodbc.connect(dbUrl)
        cursor = conn.cursor()

        # Delete the reservation entry
        delete_query = "DELETE FROM ReservationTable WHERE reservation_id = ?"
        cursor.execute(delete_query, reservation_id)
        conn.commit()

        # Close database connections
        cursor.close()
        conn.close()

        # Check if any rows were affected
        if cursor.rowcount == 0:
            return func.HttpResponse(
                f"No reservation found with ID {reservation_id}.",
                status_code=404,
            )
        
        logging.info(f"Menu Deleted Successfully.")    
        return func.HttpResponse(
            f"Reservation with ID {reservation_id} deleted successfully.",
            status_code=200,
        )
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            f"An error occurred while processing your request: {e}",
            status_code=500
        )
    