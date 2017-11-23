from utils import db_factory_func


@db_factory_func()
def init_student_table(conn):
    """
    Hello this is a documentation.
    """
    try:
        conn.execute('SELECT * FROM student')
    except Exception as e:
        print(e)
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
    """
    Hello this is a documentation.
    """
    return conn.execute('SELECT * FROM student')


@db_factory_func()
def create_student(conn, data):
    conn.execute('''INSERT INTO student 
        (id, name, username, email, faculty, token) 
        VALUES 
        (%(id)s, %(name)s, %(username)s, %(email)s, %(faculty)s, %(token)s)''', data)


@db_factory_func()
def find_one_student_by_id(conn, sid):
    return conn.execute('SELECT * FROM student WHERE id = %s', sid)


@db_factory_func()
def update_student(conn, data, sid):
    q_where = ('WHERE id=\'%s\'' % sid)
    values = ()
    placeholder = []
    for d in data:
        values = values + (data[d],)
        placeholder.append(d + '=' + '%s')
    placeholder = str.join(',', placeholder)
    q = 'UPDATE student SET ' + placeholder + q_where + 'RETURNING id'
    return conn.execute(q, values)


@db_factory_func()
def validate_token(conn, token):
    return conn.execute('SELECT * FROM student WHERE token = %s', token)


@db_factory_func()
def remove_token(conn, token):
    return conn.execute('UPDATE student SET token=null WHERE token = %s', token)
