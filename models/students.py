from utils import db_factory_func


@db_factory_func()
def init_student_table(conn):
    try:
        conn.execute('SELECT * FROM student')
    except:
        # TODO: Rethink the student model.
        conn.execute('''
            CREATE TABLE student (
                id CHAR(9) PRIMARY KEY,
                username VARCHAR(80),
                name VARCHAR(80),
                email VARCHAR(80) UNIQUE NOT NULL,
                faculty INTEGER,
                token VARCHAR(100)
            )
        ''')


@db_factory_func()
def list_students(conn):
    return conn.execute('SELECT * FROM student')


@db_factory_func()
def create_student(conn, data):
    conn.execute('''INSERT INTO student 
        (id, name, email, faculty) 
        VALUES 
        (%(id)s, %(name)s, %(username)s, %(email)s, %(faculty)s)''', data)


@db_factory_func()
def find_one_student_by_id(conn, _id):
    print(_id)
    return conn.execute('SELECT * FROM student WHERE id = %s', _id)


@db_factory_func()
def update_student(conn, data, _id):
    q_where = (' WHERE id=%s' % _id)

    values = ()
    placeholder = []
    for d in data:
        values = values + (data[d],)
        placeholder.append(d + '=' + '%s')
    placeholder = str.join(',', placeholder)
    q = 'UPDATE student SET ' + placeholder + q_where
    return conn.execute(q, values)


@db_factory_func()
def validate_token(conn, token):
    return conn.execute('SELECT * FROM student WHERE token = %s', token)


@db_factory_func()
def remove_token(conn, token):
    return conn.execute('UPDATE student SET token=null WHERE token = %s', token)
