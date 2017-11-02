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
                member_1 INTEGER DEFAULT NULL,
                member_2 INTEGER DEFAULT NULL,
                member_3 INTEGER DEFAULT NULL,

                FOREIGN KEY group_admin REFERENCES student(id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY member_1 REFERENCES student(id) ON DELETE SET NULL ON UPDATE CASCADE,
                FOREIGN KEY member_2 REFERENCES student(id) ON DELETE SET NULL ON UPDATE CASCADE, 
                FOREIGN KEY member_3 REFERENCES student(id) ON DELETE SET NULL ON UPDATE CASCADE,
            )
        ''')

@db_factory_func()
def list_chatRooms(conn):
    return conn.execute('SELECT id FROM chatgroups')

@db_factory_func()
def create_chatgroup(conn, admin_id):
    conn.execute('''INSERT INTO chatgroups
    (group_id)
    VALUES
    (%s)
    )''' % admin_id)
    return 'Chatgroup created'

@db_factory_func()
def remove_chatgroup(conn, group_id):
    # TODO: Require auth from group admin
    conn.execute("DELETE FROM chatgroups WHERE id = %s",  group_id)
    return "Group %s is removed",  group_id


# TODO
#@db_factory_func() 
#def add_member(conn, group_id, student_id):

#def remove_member