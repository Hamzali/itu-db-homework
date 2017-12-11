"""
Study Group  and Study Group - Student Model
"""
from models.base_model import BaseModel, db_factory_func


class StudyGroupModel(BaseModel):
    """
    Study group database methods.
    """

    def __init__(self, init_table=False):
        """
        Study Group database create method.
        """
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

    @db_factory_func
    def get_available_study_groups(self, conn=None, studentid="", courseids=None, date_start=None, date_end=None):
        """
        Finds and returns all available study groups for a student from database.
        """
        return conn.execute("""
            SELECT * FROM studygroup WHERE 
            (not created_by = '{}') and 
            (course in ({})) and 
            (study_date between {} and {}) and 
            id NOT IN (
                SELECT course from student_studygroup WHERE student = '{}'
            )
        """.format(studentid, str.join(", ", courseids), date_start, date_end, studentid))


class StudentStudyGroup(BaseModel):
    """
    Relation between student and study groups.
    """

    def __init__(self, init_table=False):
        """
        Table create method.
        """
        super().__init__("student_studygroup", {
            "student": "CHAR(9) NOT NULL REFERENCES student(id)",
            "studygroup": "INT NOT NULL",
            "status": "INT DEFAULT 0",  # 0 pending 1 accepted 2 rejected
            "created_at": "TIMESTAMP DEFAULT now()"
        }, primary_key=["student", "studygroup"], init_table=init_table)

    @db_factory_func
    def list_studygroup_students(self, conn=None, studygroupid=None):
        """
        Finds and joins all the student data of a study group.
        """
        return conn.execute("""
            SELECT id, username FROM student WHERE id IN 
            (SELECT student FROM studygroup JOIN student_studygroup ON(studygroup=id))
            """.format(studygroupid))
            
    @db_factory_func
    def list_studygroups_of_student(self, conn=None, studentid=None):
        """
        Finds and joins all the student data of a study group.
        """
        return conn.execute("""
            SELECT * FROM student_studygroup INNER JOIN studygroup ON studygroup=id WHERE student = '{}'
            """.format(studentid))

    def set_student_status(self, studygroup, studentid, status):
        """
        Changes the status of a student.
        """
        return self.update(query="""
            studygroup = {} and student = {}
        """.format(studygroup, studentid), data={"status": status}, return_cols=["student", "status"])[0]

    def find_student_studygroups(self, studentid):
        """
        Finds all the study groups created by a student.
        """
        return self.find(query=("created_by='%s'" % studentid))
