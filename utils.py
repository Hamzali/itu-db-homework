from server import db


def db_factory_func():
    def decorator(fn):
        def wrapper(*args, **kw):
            try:
                conn = db.engine.connect()
                result = fn(conn, *args, **kw)
                if result is not None:
                    return [dict(r) for r in result]
                return result
            finally:
                if conn is not None:
                    conn.close()

        return wrapper
    return decorator
