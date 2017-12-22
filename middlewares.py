import json
from flask import request
from functools import wraps

def auth_func(student_model):
    """
    Decarotor for student authentication.
    """
    def private_route(fn):
        @wraps(fn)
        def wrapper(*args, **kw):
            try:
                result = student_model.validate_token(request.headers["token"])
                if len(result) == 1:
                    return fn(student=result[0], *args, **kw)
                else:
                    return json.dumps({"message": "Login to proceed!"}), 401
            except Exception as e:
                print(e)
                return json.dumps({"message": "Please provide a token"}), 400
        return wrapper
    return private_route
