from server import app, db
from models.students import Result

@app.route('/students')
def createStudents():
    db.create_all()
    db.session.add(Result('Hamza ali'))
    db.session.commit()
    return 'Student endpoints model function: '
