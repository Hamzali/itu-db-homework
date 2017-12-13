"""
Building and Course - Building Relation Model
"""
from models.base_model import BaseModel

class BuildingModel(BaseModel):
    """
    Building CRUD operations for courses.
    """

    def __init__(self, init_table=False):
        super().__init__("building", {
            "id": "SERIAL PRIMARY KEY",
            "name": "VARCHAR(80) NOT NULL",
            "code": "VARCHAR(10) NOT NULL"
        }, init_table=init_table)

class CourseBuildingModel(BaseModel):
    """
    Building CRUD operations for courses.
    """

    def __init__(self, init_table=False):
        super().__init__("course_building", {
            "course": "INT NOT NULL REFERENCES course(crn)",
            "building": "INT NOT NULL REFERENCES building(id)",
            "start_time": "INT CHECK (start_time >= 0 and start_time <= 2400) NOT NULL",
            "end_time": "INT CHECK (start_time >= 0 and start_time <= 2400) NOT NULL",
            "day": "INT NOT NULL CHECK (day >= 0 and day <= 6) DEFAULT 0"
        }, primary_key=["course", "building", "day", "start_time"], init_table=init_table)
