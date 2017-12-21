from models.base_model import BaseModel


class CommentsModel(BaseModel):
    """
    Implements the comment model
    """
    def __init__(self, init_table=False):
        super().__init__("comments", {
            "id": "SERIAL PRIMARY KEY",
            "comment": "VARCHAR(500)",
            "comment_by": '''CHAR(9) REFERENCES STUDENT(id) ON DELETE SET NULL''',
            "comment_to": '''CHAR(9) REFERENCES STUDENT(id) ON DELETE SET NULL''',  # TODO ADD REFERENCES
            "made_at": "TIMESTAMP DEFAULT now()"}, init_table=init_table)
    
    def addComment(self, data):
        """
        Adds comment to given student
        """
        return self.create(data=data)
    
    def showCommentsOfStudent(self, data):
        """
        Returns a dictionary that containing comments of student
        """
        return self.find(return_cols=["comment", "id", "comment_by"],
                         query="comment_to = '%(comment_to)s'" % data)

    def updateComment(self, data):
        return self.update(query="id = %(id)s" % data, data=data)

    def removeComment(self, data):        
        return self.delete_by_id(_id=data['id'])
