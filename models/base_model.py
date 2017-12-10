"""
Models initializer.
"""
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from server import app
from utils import time_to_json
from errors import DataBaseException

DB = SQLAlchemy(app)


def db_factory_func(func):
    """
    Database connection decorator.
    """
    @wraps(func)
    def wrapper(*args, **kw):
        """
        Wrapper function for database operations.
        """
        try:
            conn = DB.engine.connect()
            result = func(conn=conn, *args, **kw)
            if result is not None:
                return [time_to_json(dict(r)) for r in result]
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
    def __init_table(self, conn=None):
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
        except Exception as sql_err:
            print(sql_err)

    @db_factory_func
    def create(self, conn=None, data=None):
        """
        Creates a and inserts a database row.
        """
        try:
            if data:
                values = []
                for field in data:
                    if self.fields.get(field) is not None:
                        values.append("%({})s".format(field))

                if values:
                    sql_statement = "INSERT INTO {} ({}) VALUES({})".format(self.table_name,
                                                                            str.join(
                                                                                ", ", data.keys()),
                                                                            str.join(", ", values))
                    try:
                        conn.execute(sql_statement, data)
                    except Exception as sql_err:
                        print(sql_err)
                        raise DataBaseException("sql query error.")
                else:
                    raise DataBaseException("data provided is not correct.")
            else:
                raise DataBaseException("data is empty.")
        except DataBaseException:
            raise

    @db_factory_func
    def find(self, conn=None, query="", limit=0, sort_by="", return_cols=None):
        """
        Finds and retrieves data with given query from database.
        """
        try:
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
                    raise DataBaseException("Invalid column selection.")
            sql_statement = "SELECT {} FROM {} ".format(
                selected_cols, self.table_name)
            if query:
                sql_statement += " WHERE {} ".format(query)
            if limit > 0:
                sql_statement += " LIMIT {} ".format(limit)
            if sort_by and self.fields.get(sort_by) is not None:
                sql_statement += " ORDER BY {} ".format(sort_by)
            try:
                return conn.execute(sql_statement)
            except Exception as sql_err:
                print(sql_err)
                raise DataBaseException("sql query error.")
        except DataBaseException:
            raise

    def find_one(self, query=""):
        """
        Finds one element from database with a given query.
        """
        return self.find(query=query, limit=1)

    def find_by_id(self, _id):
        """
        Finds one element from database with a given id.
        """
        return self.find_one(query="id=%s" % _id)

    @db_factory_func
    def update(self, conn=None, data=None, query="", return_cols=None):
        """
        Finds and updates the rows with given query.
        """
        try:
            if data:
                sql_statement = "UPDATE {} SET ".format(self.table_name)

                values = []
                for field in data:
                    if self.fields.get(field) is not None:
                        values.append("{}=%({})s".format(field, field))

                if values:
                    sql_statement += str.join(", ", values)
                else:
                    raise DataBaseException("No valid field is provided.")

                if query:
                    sql_statement += " WHERE {} ".format(query)

                if return_cols:
                    return_cols = [
                        col for col in return_cols if col in self.fields.keys()]
                    if return_cols:
                        sql_statement += " RETURNING {} ".format(
                            str.join(", ", return_cols))
                    else:
                        raise DataBaseException("Invalid column return!")

                try:
                    return conn.execute(sql_statement, data)
                except Exception as sql_err:
                    print(sql_err)
                    raise DataBaseException("sql query error.")
            else:
                raise DataBaseException("No data to update.")
        except DataBaseException:
            raise

    def update_by_id(self, _id, data=None, return_cols=None):
        """
        Update a row with id.
        """
        return self.update(data=data, query=("id=%s" % _id), return_cols=return_cols)[0]

    @db_factory_func
    def delete(self, conn=None, query="", return_cols=None):
        """
        Deletes a row with given query.
        """
        sql_statement = "DELETE FROM {} ".format(self.table_name)
        if query:
            sql_statement += " WHERE {} ".format(query)
        if return_cols:
            return_cols = [
                col for col in return_cols if col in self.fields.keys()]
            if return_cols:
                sql_statement += " RETURNING {} ".format(str.join(", ", return_cols))
            else:
                raise DataBaseException("Invalid field return!")
        try:
            return conn.execute(sql_statement)
        except Exception as sql_err:
            print(sql_err)
            raise DataBaseException("sql query error.")

    def delete_by_id(self, _id, return_cols=None):
        """
        Deletes a row with the given id.
        """
        return self.delete(query=("id=%s" % _id), return_cols=return_cols)[0]
