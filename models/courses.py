from models.base_model import BaseModel

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