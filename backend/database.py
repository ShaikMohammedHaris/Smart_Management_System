import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    BASE_DIR,
    "database",
    "queue.db"
)


def get_db_connection():

    os.makedirs(
        os.path.dirname(DATABASE),
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_db_connection()

    cursor = connection.cursor()



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT DEFAULT 'user'

        )
    """)


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queues (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            queue_name TEXT NOT NULL,

            service_type TEXT NOT NULL,

            active_counters INTEGER DEFAULT 1,

            average_service_time REAL DEFAULT 5,

            people_waiting INTEGER DEFAULT 0,

            status TEXT DEFAULT 'active'

        )
    """)


    columns = cursor.execute(
        "PRAGMA table_info(queues)"
    ).fetchall()

    column_names = [
        column["name"]
        for column in columns
    ]

    if "people_waiting" not in column_names:

        cursor.execute("""
            ALTER TABLE queues
            ADD COLUMN people_waiting INTEGER DEFAULT 0
        """)



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue_entries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            queue_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL,

            token_number INTEGER NOT NULL,

            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            status TEXT DEFAULT 'waiting'

        )
    """)



    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            queue_id INTEGER NOT NULL,

            queue_length INTEGER NOT NULL,

            active_counters INTEGER NOT NULL,

            average_service_time REAL NOT NULL,

            predicted_waiting_time REAL NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)



    cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            name,
            email,
            password,
            role
        )
        VALUES (?, ?, ?, ?)
    """, (
        "Administrator",
        "admin@gmail.com",
        "admin123",
        "admin"
    ))


    connection.commit()

    connection.close()



if __name__ == "__main__":

    initialize_database()

    print("Database initialized successfully.")