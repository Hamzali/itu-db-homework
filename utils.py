from server import db
from functools import wraps


def db_factory_func(fn):
        """
        DB connection decorator.
        """
        @wraps(fn)
        def wrapper(*args, **kw):
            try:
                conn = db.engine.connect()
                result = fn(conn=conn, *args, **kw)
                if result is not None:
                    return [dict(r) for r in result]
                return result
            finally:
                if conn is not None:
                    conn.close()

        return wrapper
