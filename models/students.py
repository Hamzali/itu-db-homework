from models.base_model import BaseModel
"""
This module creates bindings to student database.
"""


class StudentModel(BaseModel):
        """
        Student model database operations.
        """
        def __init__(self, init_table=False):
            super().__init__("student", {
                "id": "CHAR(9) PRIMARY KEY",
                "username": "VARCHAR(80) NOT NULL",
                "name": "VARCHAR(80) NOT NULL",
                "email": "VARCHAR(80) UNIQUE NOT NULL",
                "faculty": "INTEGER",
                "token": "VARCHAR(100)",
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
            return self.delete(query="token='%s'" % token)


student_model = StudentModel(init_table=True)
