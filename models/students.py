"""
Student Model
"""
from models.base_model import BaseModel


class StudentModel(BaseModel):
    """
    Student CRUD operations.
    """

    def __init__(self, init_table=False):
        super().__init__("student", {
            "id": "CHAR(9) PRIMARY KEY",
            "username": "VARCHAR(80) NOT NULL",
            "name": "VARCHAR(80) NOT NULL",
            "email": "VARCHAR(80) UNIQUE NOT NULL",
            "faculty": "INT REFERENCES faculty(id)",
            "token": "VARCHAR(100)",
            "study_start": "TIMESTAMP",
            "study_end": "TIMESTAMP",
            "created_at": "TIMESTAMP DEFAULT now()"
        }, init_table=init_table)

    def validate_token(self, token):
        """
        Finds the token and returns the user.
        """
        return self.find(query="token='%s'" % token)

    def remove_token(self, token):
        """
        Removes the authentication token from the database.
        """
        return self.update(query=("token='%s'" % token), data={"token": "NULL"}, return_cols=["id"])
