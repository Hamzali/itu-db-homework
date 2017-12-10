from models.base_model import BaseModel, db_factory_func


class HomeworksModel(BaseModel):
    """
    Implements the homeworks model
    """
    def __init__(self, init_table=False):
        super().__init__("homeworks", {
            "id": "SERIAL PRIMARY KEY",
            "crn": "INT ",  # TODO REFERENCES courses(crn)
            "name": "VARCHAR(80) NOT NULL",
            "description": "VARCHAR(500)",
            "deadline": "CHAR(10)",  # TODO: YYYY-MM-DD
            "created_by": "CHAR(9) REFERENCES student(id)"
        }, init_table=init_table)
    
    def addHomework(self, data):
        return self.create(data=data)

    def listHomeworks(self, data):
        return self.find(return_cols=["id", "crn"])

    def changeHomework(self, data):
        return self.update(data)

    def removeHomework(self, data):
        return self.delete(data)

    @db_factory_func
    def getLastHwCreatedById(self, conn, data):
        return conn.execute('''SELECT id from homeworks WHERE created_by = '%s'
                                ORDER BY id DESC LIMIT 1''' % data)


class HomeworksOfStudentModel(BaseModel):
    """
    Implements the homeworks model
    """
    def __init__(self, init_table=False):
        super().__init__("hwofstudents",{
            "student_id": '''CHAR(9) REFERENCES student(id) 
                             ON DELETE CASCADE ON UPDATE CASCADE''',
            "homework_id": "INTEGER REFERENCES homeworks(id)"
        }, init_table=init_table)

    def addHomeworkOfStudent(self, data):
        return self.create(data=data)

    @db_factory_func
    def showHomeworks(self, conn, data):
        return conn.execute('''SELECT homework_id, crn, name,
                                description, deadline FROM homeworks
                                JOIN hwofstudents
                                ON(homeworks.id=homework_id)
                                WHERE student_id='%s'
                                LIMIT 4''' % data)
    
    def removeStudentsHomework(self, data):
        self.delete(data)
