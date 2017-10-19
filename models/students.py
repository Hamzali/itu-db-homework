from server import db

def init_student_table():
    conn = db.engine.connect()
    try:
        conn.execute('SELECT * FROM student')
        return 'Table already exists!'
    except:
        conn.execute('''
            CREATE TABLE student (
                id SERIAL PRIMARY KEY,
                itu_id CHAR(9),
                name VARCHAR(80),
                email VARCHAR(80),
                phone CHAR(7),
                country_code VARCHAR(4),
                faculty INTEGER,
                token VARCHAR(100)
            )
        ''')
    finally:
        conn.close()

def list_students():
    conn = db.engine.connect()
    try:
        return conn.execute('SELECT * FROM student')
    except:
        conn.rollback()
    finally:
        conn.close()

def create_student(data):
    conn = db.engine.connect()
    try:
        conn.execute('''INSERT INTO student 
            (itu_id, name, email, phone, country_code, faculty) 
            VALUES 
            (%(itu_id)s, %(name)s, %(email)s, %(phone)s, %(country_code)s, %(faculty)s)''', data)
        return 'Student created!'
    except:
        # conn.rollback()
        return 'Failed'
    finally:
        conn.close()

def find_one_student(id='', name='', itu_id=''):
    return 'func for finding a student'