"""
Models
"""
from functools import wraps
from flask_sqlalchemy import SQLAlchemy


def init_models(app):
    """
    Models initializer.
    """
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

    models = {}

    class FacultyModel(BaseModel):
        """
        Building CRUD operations for courses.
        """

        def __init__(self, init_table=False):
            super().__init__("faculty", {
                "id": "SERIAL PRIMARY KEY",
                "name": "VARCHAR(80) NOT NULL",
                "code": "VARCHAR(10) NOT NULL"
            }, init_table=init_table)
    models["faculty"] = FacultyModel(init_table=True)

    class StudentModel(BaseModel):
        """
        Student model database operations.
        """

        def __init__(self, init_table=False):
            super().__init__("student", {
                "id": "CHAR(9) PRIMARY KEY",
                "username": "VARCHAR(80) NOT NULL",
                "name": "VARCHAR(80) NOT NULL",
                "email": "VARCHAR(80) UNIQUE NOT NULL",
                "faculty": "INT REFERENCES faculty(id)",
                "token": "VARCHAR(100)",
                "created_at": "TIMESTAMP DEFAULT now()"
            }, init_table=init_table)

        def validate_token(self, token):
            """
            Finds the token and returns the user.
            """
            return self.find(query="token='%s'" % token)

        def remove_token(self, token):
            """
            Removes the authentication token from the database.
            """
            return self.delete(query="token='%s'" % token)

    models["student"] = StudentModel(init_table=True)

    class CourseModel(BaseModel):
        def __init__(self, init_table=False):
            super().__init__("course", {
                "crn": "INT PRIMARY KEY",
                "name": "VARCHAR(80) NOT NULL",
                "code": "VARCHAR(10) NOT NULL",
                #"instructor": "",  # TODO: foreign key for Instructor
            }, init_table=init_table)

        def course_exists(self, courseid):
            """
            Checks if a course exists.
            """
            result = self.find(query=("crn=%s" % courseid))
            if not result:
                return True
            return False

    models["course"] = CourseModel(init_table=True)

    class BuildingModel(BaseModel):
        """
        Building CRUD operations for courses.
        """

        def __init__(self, init_table=False):
            super().__init__("building", {
                "id": "SERIAL PRIMARY KEY",
                "name": "VARCHAR(80) NOT NULL",
                "code": "VARCHAR(10) NOT NULL"
            }, init_table=init_table)
    models["building"] = BuildingModel(init_table=True)

    class CourseBuildingModel(BaseModel):
        """
        Building CRUD operations for courses.
        """

        def __init__(self, init_table=False):
            super().__init__("course_building", {
                "course": "INT NOT NULL REFERENCES course(crn)",
                "building": "INT NOT NULL REFERENCES building(id)",
                "start_time": "INT(9999, 4) NOT NULL",
                "end_time": "INT(9999, 4) NOT NULL",
                "day": "INT NOT NULL CHECK (day >= 0 and day <= 6)"
            }, primary_key=["course", "building", "day", "start_time"], init_table=init_table)
    models["course_building"] = CourseBuildingModel(init_table=True)

    class StudentCourseModel(BaseModel):
        """
        Building CRUD operations for courses.
        """

        def __init__(self, init_table=False):
            super().__init__("student_course", {
                "course": "INT NOT NULL REFERENCES course(crn)",
                "student": "CHAR(9) NOT NULL REFERENCES student(id)",
                "created_at": "TIMESTAMP DEFAULT now()"
            }, primary_key=["course", "student"], init_table=init_table)
    models["student_course"] = StudentCourseModel(init_table=True)

    class StudyGroupModel(BaseModel):
        """

        """

        def __init__(self, init_table=False):
            super().__init__("studygroup", {
                "id": "SERIAL PRIMARY KEY",
                "name": "VARCHAR(20) NOT NULL",
                "description": "VARCHAR(100)",
                "course": "INT NOT NULL REFERENCES course(crn)",
                "study_date": "TIMESTAMP NOT NULL",
                "duration": "INT NOT NULL CHECK (duration <= 10 and duration >= 0)",
                "student_count": "INT DEFAULT 0",
                # "location": "",
                "created_by": "CHAR(9) NOT NULL REFERENCES student(id)",
                "created_at": "TIMESTAMP DEFAULT now()"
            }, init_table=init_table)
        def get_available_study_groups(self, studentid,  courseid, date_start, date_end):
            return self.find("""
                (not created_by = {}) and (course = {}) and (study_date > {} and study_date < {})
            """.format(studentid, courseid, date_start, date_end))

    models["studygroup"] = StudyGroupModel(init_table=True)

    class StudentStudyGroup(BaseModel):
        def __init__(self, init_table=False):
            super().__init__("student_studygroup", {
                "student": "CHAR(9) NOT NULL REFERENCES student(id)",
                "studygroup": "INT NOT NULL",
                "status": "INT DEFAULT 0", # 0 pending 1 accepted 2 rejected
                "created_at": "TIMESTAMP DEFAULT now()"
            }, primary_key=["student", "studygroup"], init_table=init_table)

        @db_factory_func
        def list_studygroup_students(self, conn, _id):
            return conn.execute("""
                SELECT id, username FROM student 
                JOIN (SELECT * FROM student_studygroup WHERE studygroup = {}) 
                ON student.id = student_studygroup.id
                """.format(_id))
        
        def set_student_status(self, studygroup, studentid, status):
            self.update(query="""
                studygroup = {} and student = {}
            """.format(studygroup, studentid), data={"status": status})

    models["student_studygroup"] = StudentStudyGroup(init_table=True)

    return models
