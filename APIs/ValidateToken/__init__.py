import azure.functions as func
import logging
import os
import jwt  # PyJWT library
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
import json


SECRET_KEY = os.environ['JWT_SECRET_KEY']

async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing a new Token Validation request.')

    try:
        req_body = req.get_json()
        token = req_body.get("token")
        if not token:
            return func.HttpResponse(
                body=json.dumps({"message": "Token is missing!"}),
                mimetype="application/json",
                status_code=401
            )
        
        try:
            # Decode the token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            
            return func.HttpResponse(
                body=json.dumps({"message": "Token is valid", "user": decoded_token}),
                mimetype="application/json",
                status_code=200
            )
        
        except ExpiredSignatureError:
            return func.HttpResponse(
                body=json.dumps({"message": "Token has expired!"}),
                mimetype="application/json",
                status_code=401
            )
        except (InvalidTokenError, DecodeError):
            return func.HttpResponse(
                body=json.dumps({"message": "Invalid token!"}),
                mimetype="application/json",
                status_code=401
            )
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return func.HttpResponse(
                body=json.dumps({"message": "Error validating token!"}),
                mimetype="application/json",
                status_code=500
            )
        
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return func.HttpResponse(
            body=f"An error occurred while processing your request: {e}",
            status_code=500
        )
