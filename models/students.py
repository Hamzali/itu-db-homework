from utils import db_factory_func


@db_factory_func()
def init_student_table(conn):
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


@db_factory_func(return_json=True)
def list_students(conn):
    return conn.execute('SELECT * FROM student')


@db_factory_func()
def create_student(conn, data):
    conn.execute('''INSERT INTO student 
        (itu_id, name, email, phone, country_code, faculty) 
        VALUES 
        (%(itu_id)s, %(name)s, %(email)s, %(phone)s, %(country_code)s, %(faculty)s)''', data)
    return 'Student created!'


@db_factory_func(return_json=True)
def find_one_student_by_id(conn, db_id=None, itu_id=None):
    if db_id is not None:
        return conn.execute('SELECT * FROM student WHERE id = %s', db_id)
    elif itu_id is not None:
        return conn.execute('SELECT * FROM student WHERE itu_id = %s', itu_id)


@db_factory_func()
def update_student(conn, db_id, data):
    values = ()
    placeholder = []
    for d in data:
        values = values + (data[d],)
        placeholder.append(d + '=' + '%s')
    placeholder = str.join(',', placeholder)
    q = 'UPDATE student SET ' + placeholder + (' WHERE %s=id' % db_id)
    conn.execute(q, values)
    return 'update student data'
