from models.students import StudentModel
from models.buildings import BuildingModel, CourseBuildingModel
from models.courses import CourseModel, StudentCourseModel
from models.faculties import FacultyModel
from models.studygroups import StudyGroupModel, StudentStudyGroup


faculty_model = FacultyModel(init_table=True)
student_model = StudentModel(init_table=True)
course_model = CourseModel(init_table=True)
building_model = BuildingModel(init_table=True)
course_building_model = CourseBuildingModel(init_table=True)
student_course_model = StudentCourseModel(init_table=True)
studygroup_model = StudyGroupModel(init_table=True)
student_studygroup_model = StudentStudyGroup(init_table=True)