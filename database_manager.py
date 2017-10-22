import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=db_lab user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM test;")
cur.fetchone()
# (1, 100, "abc'def")

# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()


def get_user_state(user_id):
    connect_string = "host='localhost' dbname='db_lab' user='meysam' password='9092301202'"
    conn = psycopg2.connect(connect_string)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    user_state = cur.fetchone()
    if user_state:
        return user_state[2]
    else:
        pass # TODO insert the new user state to database
