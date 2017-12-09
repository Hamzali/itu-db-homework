"""
Models initializer.
"""
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from server import app

db = SQLAlchemy(app)

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

class BaseModel:
    """
    Base class for the data manipulation and database operations.
    """
    def __init__(self, table, fields, primary_key=None, init_table=False):
        self.table_name = table
        self.fields = fields
        self.primary_key = primary_key
        if init_table:
            self.__init_table()

    @db_factory_func
    def __init_table(self, conn):
        """
        Initializes the database.
        """
        try:
            result = conn.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema='public'
                AND table_type='BASE TABLE';
            """)

            result = [dict(r) for r in result]
            result = [r.get("table_name") for r in result]

            if self.table_name not in result:
                table_fields = []
                for field in self.fields:
                    table_fields.append(field + " " + self.fields[field])

                if self.primary_key:
                    table_fields.append(
                        "PRIMARY KEY (" + str.join(", ", self.primary_key) + ")")
                init_query = "CREATE TABLE {} ( {} )".format(
                    self.table_name, str.join(", ", table_fields))
                conn.execute(init_query)
        except Exception as e:
            print(e)

    @db_factory_func
    def create(self, conn, data):
        values = []
        for field in data:
            if self.fields.get(field) is not None:
                values.append("%({})s".format(field))

        if values:
            sql_statement = """INSERT INTO {}
                            ({}) 
                            VALUES 
                            ({}) 
                            """.format(self.table_name, str.join(", ", data.keys()), str.join(", ", values))
            conn.execute(sql_statement, data)
        else:
            # TODO: handle the error more gracefully.
            print("Please give fields in order to create.")

    @db_factory_func
    def find(self, conn, query="", limit=0, sort_by="", return_cols=None):
        selected_cols = "*"
        if return_cols:
            selected_cols = []
            for col in return_cols:
                if self.fields.get(col) is not None:
                    selected_cols.append(col)
                else:
                    print("%s is not a valid column name!" % col)
            if selected_cols:
                selected_cols = str.join(",", selected_cols)
            else:
                # TODO: handle the error elegantly.
                print("There is no valid column name!")
                selected_cols = "*"
        sql_statement = "SELECT {} FROM {} ".format(
            selected_cols, self.table_name)
        if query:
            sql_statement += " WHERE {} ".format(query)
        if limit > 0:
            sql_statement += " LIMIT {} ".format(limit)
        if sort_by and self.fields.get(sort_by) is not None:
            sql_statement += " ORDER BY {} ".format(sort_by)
        return conn.execute(sql_statement)

    def find_one(self, query=""):
        return self.find(query=query, limit=1)

    def find_by_id(self, _id):
        return self.find_one(query="id=%s" % _id)

    @db_factory_func
    def update(self, conn, data={}, query="", returning_id=True):
        sql_statement = "UPDATE {} SET ".format(self.table_name)

        values = []
        for field in data:
            if self.fields.get(field) is not None:
                values.append("{}=%({})s".format(field, field))
        sql_statement += str.join(", ", values)

        if query:
            sql_statement += " WHERE {} ".format(query)

        if returning_id:
            sql_statement += "RETURNING id"

        return conn.execute(sql_statement, data)

    def update_by_id(self, _id, data={}):
        return self.update(data=data, query=("id=%s" % _id))

    @db_factory_func
    def delete(self, conn, query="", returning_id=True):
        sql_statement = "DELETE FROM {} ".format(self.table_name)
        if query:
            sql_statement += " WHERE {} ".format(query)
        else:
            sql_statement += "* "
        if returning_id:
            sql_statement += "RETURNING id"
        return conn.execute(sql_statement)

    def delete_by_id(self, _id):
        return self.delete(query=("id=%s" % _id))
