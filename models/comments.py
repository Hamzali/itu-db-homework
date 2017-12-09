from models.base_model import BaseModel


class CommentsModel(BaseModel):
    """
    Implements the comment model 
    """
    def __init__(self, init_table=False):
        super().__init__("comments", {
            "id": "SERIAL PRIMARY KEY",
            "comment": "VARCHAR(500)",
            "comment_by": '''CHAR(9) ''',
            "comment_to": '''CHAR(9) ''',  # TODO ADD REFERENCES
            "made_at": "TIMESTAMP"}, init_table)
    
    def addComment(self, data):
        return self.create(data)
    
    def showCommentsOfStudent(self, data):
        return self.find(query="comment_to = %(comment_to)s::CHAR(9)" % data)

    def updateComment(self, data):
        return self.update(query="id = %(id)s" % data, data=data)

    def removeComment(self, data):
        return self.delete_by_id(_id=data['id'])


commentsTable = CommentsModel(init_table=True)
