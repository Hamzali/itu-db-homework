from models.base_model import BaseModel


class CourseModel(BaseModel):
	def __init__(self, init_table=False):
		super().__init__("course", {
			"id": "CHAR(5) PRIMARY KEY",
			"name": "VARCHAR(80) NOT NULL",
			"code": "VARCHAR(7) NOT NULL",
			"day": "",
			"hours": "",
			"instructor": "",  # TODO: foreign key for Instructor
			"faculty": "",  # TODO: Create a table for Faculties.
			"building": ""  # TODO: Create a table for Buildings.
		}, init_table)


course_model = CourseModel(init_table=True)
