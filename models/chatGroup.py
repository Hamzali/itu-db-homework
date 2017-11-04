from utils import db_factory_func

@db_factory_func()
def init_chatGroup_table(conn):
    try:
        conn.execute("SELECT * FROM chatgroups")
        return "It does exists!"
    except:
        conn.execute('''
            CREATE TABLE chatgroups (
                id SERIAL PRIMARY KEY,
                group_admin INTEGER,
                name VARCHAR(80),
                created_at TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY group_admin REFERENCES student(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY created_by REFERENCES student(id) ON DELETE SET NULL ON UPDATE CASCADE
                
            )
        ''')
@db_factory_func()
def init_studentsOnChat_table(conn):
    try:
        conn.execute("SELECT * FROM studentsOnChat")
        return "It does exists!"
    except:
        conn.execute('''
            CREATE TABLE studentsOnChat (
                chatgroup_id INTEGER,
                student_id INTEGER,
                FOREIGN KEY student_id REFERENCES student(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY chatgroup_id REFERENCES chatgroups(id) ON DELETE CASCADE,
                UNIQUE(student_id, chatgroup_id)

            )
        
        ''')

@db_factory_func()
def list_chatRooms(conn):
    return conn.execute('SELECT id FROM chatgroups')

@db_factory_func()
def create_chatgroup(conn, admin_id, name):
    if len(name) < 80 and name is not None:
        conn.execute('''INSERT INTO chatgroups
        (group_admin, name, created_by)
        VALUES
        (%s, %s, %s)
        )''' % admin_id, name, admin_id)
        return 'Chatgroup created'
    else:
        return 'Name field can not be empty or have length more than 80!'

@db_factory_func()
def remove_chatgroup(conn, group_id):
    # TODO: Require auth from group admin
    conn.execute("DELETE FROM chatgroups WHERE id = %s" %  group_id)
    return "Group %s is removed" %  group_id


@db_factory_func() 
def add_member(conn, group_id, student_id):
    # TODO: Require auth from the student to be added
    conn.execute('''
        INSERT INTO studentsOnChat (
            VALUES(
                %s, %s
            )
        )
        
        ''' %s group_id, student_id)

@db_factory_func()
def remove_member(conn, group_id, student_id)
    # TODO: Require auth from the student to be removed or admin auth
    conn.execute('''
        DELETE FROM studentsOnChat WHERE chatgroup_id=%s AND student_id = %s
    ''' % group_id, student_id)

@db_factory_func()
def show_groups_of_student(conn, student_id)
    return conn.execute('''
        SELECT * FROM chatgroups JOIN studentsOnChat ON(chatgroups.id=studentsOnChat.chatgroup_id)
        WHERE student_id = %s
)''' % student_id )
