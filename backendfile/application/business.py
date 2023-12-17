from werkzeug.exceptions import HTTPException
from flask import make_response, jsonify
class BusinessValidationError(HTTPException):
    def __init__(self, statuscode, errormessage):
        data = {"errormessage": errormessage }
        self.response = make_response(jsonify(data), statuscode)