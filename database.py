import sqlite3

DB_NAME = "captcha_results.db"


def initialize_database():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_type TEXT,
            challenge TEXT,
            answer TEXT,
            result TEXT,
            execution_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully!")


def save_experiment(
    challenge_type,
    challenge,
    answer,
    result,
    execution_time
):
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        INSERT INTO experiments
        (
            challenge_type,
            challenge,
            answer,
            result,
            execution_time
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        challenge_type,
        challenge,
        answer,
        result,
        execution_time
    ))

    connection.commit()
    connection.close()
