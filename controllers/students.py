from models.students import createStudent

def studentsController(app, db):
    @app.route('/students')
    def getStudents():
        return 'Student endpoints model function: ' + createStudent(db)