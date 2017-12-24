import psycopg2

connect_string = "host='localhost' dbname='db_lab' user='postgres' password='9092301202'"

"""""
just kept for sample
# Execute a command: this creates a new table
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
cur.fetchone()
# (1, 100, "abc'def")
"""""


def get_user_state(user_id):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user_state = cur.fetchone()
    if user_state:
        res = user_state[2]
    else:
        cur.execute("INSERT INTO users (user_id, state) VALUES (%s, %s)", (user_id, 'initial'))
        res = 'initial'

    conn.commit()
    cur.close()
    conn.close()

    return res


def set_user_state(user_id, state):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("UPDATE users SET state=%s WHERE user_id=%s", (state, user_id,))
    conn.commit()
    cur.close()
    conn.close()


def add_class(class_number, cap, des):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("INSERT INTO classroom (number, cap, description) VALUES (%s,%s,%s)",
                (class_number, cap, des))
    conn.commit()
    cur.close()
    conn.close()


def add_teacher(f_name, l_name):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("SELECT add_teacher(%s,%s);", (f_name, l_name))
    conn.commit()
    cur.close()
    conn.close()


def get_teachers_list():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("SELECT * FROM teacher;")

    t_list = []
    for row in cur:
        t_list.append(row[1] + ' ' + row[2])

    conn.commit()
    cur.close()
    conn.close()

    return t_list


def find_and_insert_class(list):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("BEGIN;")
    cur.execute("SAVEPOINT my_savepoint;")
    if len(list) != 3:
        cur.execute("ROLLBACK TO my_savepoint;")
    else:
        cur.execute("SELECT * from classroom;")
        all_classes = []
        for row in cur:
            if row[3]:  # if class is available
                all_classes.append(row[1])
        print("all classes: " + str(all_classes))

        cur.execute('SELECT class_number FROM assigned_classes '
                    'WHERE week_number=%s '
                    'and time_number=%s;',
                    (list[1], list[2]))
        busy_classes = []
        for row in cur:
            busy_classes.append(row[0])
        print("busy classes: " + str(busy_classes))

        for classroom in busy_classes:
            all_classes.remove(classroom)

        if len(all_classes) < 1:
            cur.execute("ROLLBACK TO my_savepoint;")
        else:

            cur.execute("INSERT INTO assigned_classes (teacher, class_number, week_number, time_number) "
                        "VALUES (%s,%s,%s,%s);",
                        (list[0], all_classes[0], list[1], list[2])
                        )
            cur.execute("COMMIT;")
            return all_classes[0]
    conn.commit()
    cur.close()
    conn.close()

    return -1


def drop_tables():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute('DROP TABLE "public".course;')
    cur.execute('DROP TABLE "public".student;')
    cur.execute('DROP TABLE "public".prof;')
    conn.commit()
    cur.close()
    conn.close()


def init():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute(
        'CREATE TABLE '
        'public.student('
        'id INT PRIMARY KEY NOT NULL,name VARCHAR(100) NOT NULL,'
        'year INT NOT NULL);'
        'CREATE UNIQUE INDEX student_id_uindex ON public.student (id);'
    )

    cur.execute(
        'CREATE TABLE '
        'public.course('
        'id VARCHAR(10) PRIMARY KEY NOT NULL,'
        'name VARCHAR(100) NOT NULL,'
        'credit INT NOT NULL);'
        'CREATE UNIQUE INDEX course_id_uindex ON public.course (id);'
    )

    cur.execute(
        'CREATE TABLE '
        'public.prof('
        'id VARCHAR(10) PRIMARY KEY NOT NULL,'
        'name VARCHAR(100) NOT NULL,'
        'salary INT NOT NULL);'
        'CREATE UNIQUE INDEX prof_id_uindex ON public.prof (id);'
    )

    conn.commit()
    cur.close()
    conn.close()


def add_student(id, name, year):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    retval = 0
    try:
        cur.execute('INSERT INTO student (id, name, "year") VALUES (%s,%s,%s)',
                    (id, name, year))
    except psycopg2.IntegrityError:
        retval = -1

    conn.commit()
    cur.close()
    conn.close()
    return retval


def add_course(id, name, credit):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    retval = 0
    try:
        cur.execute('INSERT INTO course (id, name, credit) VALUES (%s,%s,%s)',
                    (id, name, credit))
    except psycopg2.IntegrityError:
        retval = -1

    conn.commit()
    cur.close()
    conn.close()
    return retval


def add_prof(id, name, salary):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    retval = 0
    try:
        cur.execute('INSERT INTO prof (id, name, salary) VALUES (%s,%s,%s)',
                    (id, name, salary))
    except psycopg2.IntegrityError:
        retval = -1

    conn.commit()
    cur.close()
    conn.close()
    return retval


def get_students():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    for val in cur:
        print(str(val[0]) + ', ' + str(val[1]) + ', ' + str(val[2]))
    conn.commit()
    cur.close()
    conn.close()


def get_courses():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM course')
    for val in cur:
        print(str(val[0]) + ', ' + str(val[1]) + ', ' + str(val[2]))
    conn.commit()
    cur.close()
    conn.close()


def get_profs():
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM prof')
    for val in cur:
        print(str(val[0]) + ', ' + str(val[1]) + ', ' + str(val[2]))
    conn.commit()
    cur.close()
    conn.close()


def search_student(name):
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    for val in cur:
        if val[1].lower().startswith(name):
            print(str(val[0]) + ', ' + str(val[1]) + ', ' + str(val[2]))
    conn.commit()
    cur.close()
    conn.close()
