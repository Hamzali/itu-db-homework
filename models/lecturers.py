from models.base_model import BaseModel
"""
This model creates lecturers model
"""


class LecturersModel(BaseModel):
    """
    Lecturer table CRUD operations.
    """
    def __init__(self, init_table=False):
        super().__init__("lecturers", {
            "id": "SERIAL PRIMARY KEY",
            "fname": "VARCHAR(80) NOT NULL",
            "sname": "VARCHAR(80) NOT NULL",
            "department": "VARCHAR(80)",
            "email": "VARCHAR(100)"
        }, init_table=init_table)
    

    def addLecturer(self, data):
        return self.create(data=data)

    def listAllLecturers(self):
        return self.find(return_cols=["fname", "sname", "id"],
                         sort_by="")
    
    def listAllLecturersBySName(self):
        return self.find(return_cols=["sname"], sort_by="sname")

    def listLecturersOfDepartment(self, data):
        return self.find(return_cols=["fname", "sname"],
                         query="department = sex")

    def showALecturer(self, data):
        return self.find(return_cols=["fname", "sname"],
                         query="id = %s" % data['id'])

    def updateLecturer(self, data):
        return self.update_by_id(data['id'])

    def removeLecturer(self, data):
        return self.delete_by_id(data['id'])
