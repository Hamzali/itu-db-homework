from models.base_model import BaseModel

class FacultyModel(BaseModel):
    """
    Faculty CRUD operations.
    """

    def __init__(self, init_table=False):
        super().__init__("faculty", {
            "id": "SERIAL PRIMARY KEY",
            "name": "VARCHAR(80) NOT NULL",
            "code": "VARCHAR(10) NOT NULL"
        }, init_table=init_table)
