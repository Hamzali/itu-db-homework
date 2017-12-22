"""
Course and Student - Course Model
"""
from models.base_model import BaseModel, db_factory_func


class CourseModel(BaseModel):
    """
    Course CRUD operations class.
    """
    def __init__(self, init_table=False):
        super().__init__("course", {
            "crn": "INT PRIMARY KEY",
            "name": "VARCHAR(80) NOT NULL",
            "code": "VARCHAR(15) NOT NULL",
            #"instructor": "",  # TODO: foreign key for Instructor
        }, init_table=init_table)

    def course_exists(self, courseid):
        """
        Checks if a course exists.
        """
        result = self.find(query=("crn=%s" % courseid))
        if result:
            return result[0]
        return False


class StudentCourseModel(BaseModel):
    """
    Student-Course Relation CRUD operations.
    """

    def __init__(self, init_table=False):
        super().__init__("student_course", {
            "course": "INT NOT NULL REFERENCES course(crn)",
            "student": "CHAR(9) NOT NULL REFERENCES student(id)",
            "created_at": "TIMESTAMP DEFAULT now()"
        }, primary_key=["course", "student"], init_table=init_table)

    @db_factory_func
    def find_student_courses(self, conn=None, studentid=None):
        """
        Finds all the courses of student with given student id.
        """
        return conn.execute("""
            SELECT crn, name, code FROM student_course INNER JOIN course 
            ON course.crn = student_course.course WHERE student = '{}' 
        """.format(studentid))

    def delete_student_course(self, studentid, courseid):
        """
        Deletes a student course row with given ids.
        """
        self.delete(query="student = '{}' and course = {}".format(
            studentid, courseid), return_cols=["course"])
