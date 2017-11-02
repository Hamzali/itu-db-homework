import json
from flask import request
from models.students import validate_token


def private_route():
    def decorator(fn):
        def wrapper(*args, **kw):
            # Check for the auth
            try:
                result = validate_token(request.headers['token'])
                print(result, request.headers['token'])
                if len(result) == 1:
                    return fn(result[0], *args, **kw)
                else:
                    return json.dumps({'message': 'Login to proceed!'}), 401
            except Exception as e:
                print(e)
                return json.dumps({'message': 'Please provide a token'}), 400
        return wrapper
    return decorator
