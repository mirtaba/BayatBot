import psycopg2

connect_string = "host='localhost' dbname='db_lab' user='meysam' password='9092301202'"

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
