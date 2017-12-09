from models.base_model import BaseModel, db_factory_func


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