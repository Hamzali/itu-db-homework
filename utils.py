from server import db
import json


def db_factory_func(return_json=None):
    def decorator(fn):
        def wrapper(*args, **kw):
            try:
                conn = db.engine.connect()
                result = fn(conn, *args, **kw)
                if return_json is not None:
                    return json.dumps([dict(r) for r in result])
                else:
                    return result
            finally:
                if conn is not None:
                    conn.close()

        return wrapper
    return decorator
