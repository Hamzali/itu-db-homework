from models.base_model import BaseModel


class CourseModel(BaseModel):
        def __init__(self, init_table=False):
            super().__init__("course", {
                "crn": "INT PRIMARY KEY",
                "name": "VARCHAR(80) NOT NULL",
                "code": "VARCHAR(7) NOT NULL",
                #"instructor": "",  # TODO: foreign key for Instructor
            }, init_table=init_table)

        def course_exists(self, courseid):
            result = self.find(query=("crn=%s" % courseid))
            if len(result) > 0:
                return True
            return False


class BuildingModel(BaseModel):
	'''
	Building CRUD operations for courses.
	'''
	def __init__(self, init_table=False):
		super().__init__("building", {
			"id": "SERIAL PRIMARY KEY",
			"name": "VARCHAR(80) NOT NULL",
			"code": "VARCHAR(10) NOT NULL"
		}, init_table=init_table)


class FacultyModel(BaseModel):
	'''
	Building CRUD operations for courses.
	'''
	def __init__(self, init_table=False):
		super().__init__("faculty", {
			"id": "SERIAL PRIMARY KEY",
			"name": "VARCHAR(80) NOT NULL",
			"code": "VARCHAR(10) NOT NULL"
		}, init_table=init_table)


class CourseBuildingModel(BaseModel):
	'''
	Building CRUD operations for courses.
	'''
	def __init__(self, init_table=False):
		super().__init__("course_building", {
			"id": "SERIAL PRIMARY KEY",
			"course": "INT NOT NULL REFERENCES course(crn)",
			"building": "INT NOT NULL REFERENCES building(id)",
			"start_time": "INT NOT NULL",
			"end_time": "INT NOT NULL",
			"day": "INT NOT NULL"
		},  init_table=init_table)


building_model = BuildingModel(init_table=True)
faculty_model = FacultyModel(init_table=True)
course_model = CourseModel(init_table=True)
courseBuilding_model = CourseBuildingModel(init_table=True)