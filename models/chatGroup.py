from models.base_model import BaseModel


class ChatGroupsModel(BaseModel):
    """
    Implements the chat feature
    """
    def __init__(self, init_table=False):
        super().__init__("chatgroups", {
            "id": "SERIAL PRIMARY KEY",
            "group_admin": '''INTEGER REFERENCES student(id) ON DELETE CASCADE
             ON UPDATE CASCADE''',
            "name": "VARCHAR(80) NOT NULL",
            "created_at": "TIMESTAMP",
            "created_by": '''INTEGER REFERENCES student(id) ON DELETE SET NULL
             ON UPDATE CASCADE '''}, init_table)
        
    def listGroups(self):
        return self.find(self, return_cols=["id", "name"], sort_by="id")

    def createGroup(self, data):
        self.create(self, data)
    
    def removeGroup(self, data):
        # TODO: Require auth from admin and error handling
        return self.delete_by_id(_id=data['id'])
    
    def updateGroup(self, data):
        return self.update(self, data)


class StudentsOnChatModel(BaseModel):
    def __init__(self, init_table=False):
        super().__init__("studentsOnChat", {
            "chatgroup_id": '''INTEGER REFERENCES chatgroups(id) 
             ON DELETE CASCADE''',
            "student_id": '''INTEGER REFERENCES student(id) ON DELETE CASCADE 
            ON UPDATE CASCADE''',
        })

    def addMember(self, data):
        self.create(self, data)
    
    # TODO: Join it with students table and get the names.
    def listMembersOfGroup(self, data):
        return self.find(self, query="chatgroup_id = %s" % data['cid'],
                         return_cols=['student_id'], sort_by='student_id')

    # TODO: Join it with chatgroups to get speficic student's group
    def showGroupsOfStudent(self, data):
        pass
    
    def checkIfMember(self, data):
        return self.find(self, query='''chatgroup_id = %(cid)s 
                         AND student_id = %(sid)s''' % data, limit=1, 
                         return_cols=['student_id'])

    def removeMember(self, data):
        return self.delete(self, query="student_id = %s" % data['sid'])

studentOnChat = StudentsOnChatModel(True)
chatGroups = ChatGroupsModel(True)