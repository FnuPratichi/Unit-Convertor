import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_ENDPOINT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT')
    )
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Example table creation
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    )
    ''')

    # Clear the table
    cursor.execute('TRUNCATE TABLE students')

    # Insert initial data
    initial_data = [
        ('Alice', 'alice@example.com', 'password1'),
        ('Bob', 'bob@example.com', 'password2'),
        ('Charlie', 'charlie@example.com', 'password3')
    ]

    insert_query = '''
    INSERT INTO students (name, email, password)
    VALUES (%s, %s, %s)
    '''

    cursor.executemany(insert_query, initial_data)

    conn.commit()
    cursor.close()
    conn.close()

    print("Database initialized successfully.")

if __name__ == '__main__':
    init_database()



# psql -h fprat-db-postgresdb-piv2tr5qphh2.cd2400460bae.us-east-1.rds.amazonaws.com -p 5432 -d db1 -U postgresuser
# \dt : to get all the tables 
# \dtable_name to get the structure 
#-- View all rows in students table
#SELECT * FROM students;

#-- View specific columns
#SELECT id, name, email FROM students;

#-- Filter data
#SELECT * FROM students WHERE name LIKE 'Alice%';

#-- Aggregate functions
#SELECT COUNT(*) AS total_students FROM students;

