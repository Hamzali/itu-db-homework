from models.base_model import BaseModel, db_factory_func


class ChatGroupsModel(BaseModel):
    """
    Implements the chat feature
    """
    def __init__(self, init_table=False):
        super().__init__("chatgroups", {
            "id": "SERIAL PRIMARY KEY",  # TODO create chatgroup for studygroup
            "group_admin": '''CHAR(9) NOT NULL REFERENCES student(id) ON DELETE CASCADE
             ON UPDATE CASCADE''',
            "name": "VARCHAR(80) NOT NULL",
            "created_at": "TIMESTAMP DEFAULT now()",
            "created_by": '''CHAR(9) REFERENCES student(id) ON DELETE SET NULL
             ON UPDATE CASCADE '''}, init_table=init_table)
        
    def listGroups(self):
        return self.find(return_cols=["id"], sort_by="id")

    def createGroup(self, data):
        self.create(data=data)
    
    def removeGroup(self, data):
        # TODO: Require auth from admin and error handling
        return self.delete_by_id(_id=data['id'])
    
    def updateGroup(self, data):
        return self.update(data=data)

    #  Returns the groups that a people manages
    def checkIsAdmin(self, data):
        return self.find(return_cols=["id"], query="group_admin = %s" % data["sid"])

    @db_factory_func
    def getLastGroupCreatedById(self, conn, data):
        return conn.execute('''SELECT id from chatgroups WHERE created_by = '%s'
                                ORDER BY created_at DESC''' % data)

class StudentsOnChatModel(BaseModel):
    def __init__(self, init_table=False):
        super().__init__("studentsonchat", {
            "chatgroup_id": '''INTEGER NOT NULL REFERENCES chatgroups(id)
             ON DELETE CASCADE''',
            "student_id": '''CHAR(9) REFERENCES student(id) ON DELETE CASCADE
             ON UPDATE CASCADE''',
            "joined_at": "TIMESTAMP DEFAULT now()"
            }, init_table=init_table)

    def addMember(self, data):
        self.create(data=data)
    
    # TODO: Join it with students table and get the names.
    def listMembersOfGroup(self, data):
        return self.find(query="chatgroup_id = %s" % data['cid'],
                         return_cols=['student_id'], sort_by='student_id')

    
    @db_factory_func
    def showGroupsOfStudent(self, conn, data):
        return conn.execute('''SELECT id FROM chatgroups JOIN studentsonchat 
                        ON(chatgroups.id=studentsonchat.chatgroup_id)
                        WHERE student_id = %s''', data)
    
    def checkIfMember(self, data):
        return self.find(query='''chatgroup_id = %(cid)s 
                         AND student_id = %(sid)s''' % data, limit=1,
                         return_cols=['chatgroup_id'])

    def removeMember(self, data):
        return self.delete(query='''student_id = (%(sid)s)::CHAR(9) AND
                            chatgroup_id = (%(cid)s)::INTEGER ''' % data,
                            returning_id=False)
