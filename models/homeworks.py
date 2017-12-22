from models.base_model import BaseModel, db_factory_func


class HomeworksModel(BaseModel):
    """
    Implements the homeworks model\n
    Keeps track of homeworks and their details but owner of homework is unknown
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
        """
        Adds new homework test
        """
        return self.create(data=data)

    def listHomeworks(self, data):
        """
        Returns a dictionary of homeworks by course identities
        """
        return self.find(return_cols=["id", "crn"])

    def changeHomework(self, hwid, data):
        """
        Alters homework information by id
        """
        self.update(query="id = %i" % hwid, data=data)
    
    def removeHomework(self, data):
        """
        Removes homework by id
        """
        return self.delete(data)

    @db_factory_func
    def getLastHwCreatedById(self, conn, data):
        """
        Returns the last homework's id of given student. Used for simultenously adding homework to student

        :param data: student_id
        """
        return conn.execute('''SELECT id from homeworks WHERE created_by = '%s'
                                ORDER BY id DESC LIMIT 1''' % data)


class HomeworksOfStudentModel(BaseModel):
    """
    Implements the homeworks of student model\n
    Allows us to see which one has which homeworks
    """
    def __init__(self, init_table=False):
        super().__init__("hwofstudents", {
            "student_id": '''CHAR(9) REFERENCES student(id)
                             ON DELETE CASCADE ON UPDATE CASCADE''',
            "homework_id": "INT"
        }, init_table=init_table)

    def addHomeworkOfStudent(self, data):
        return self.create(data=data)

    @db_factory_func
    def showHomeworks(self, conn, data):
        """
        Shows homeworks of specific student

        :param data: Student information
        """
        return conn.execute('''SELECT homework_id, crn, name,
                                description, deadline FROM homeworks
                                JOIN hwofstudents
                                ON(homeworks.id=homework_id)
                                WHERE student_id='%s'
                                ORDER BY homework_id DESC LIMIT 4 ''' % data)
    
    @db_factory_func
    def removeStudentsHomework(self, conn, data):
        conn.execute('''DELETE FROM hwofstudents WHERE student_id = '%(sid)s'
                        AND homework_id = %(homework_id)i''' % data)    
        