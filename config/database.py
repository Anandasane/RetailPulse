
import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "username": "root",
    "password": os.getenv("RETAILPULSE_DB_PASSWORD"),
    "database": "retailpulse"
}


def get_engine():

    if not DB_CONFIG["password"]:
        raise ValueError(
            "RETAILPULSE_DB_PASSWORD environment variable is not set."
        )

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_CONFIG["username"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"]
    )

    return create_engine(
        connection_url,
        pool_pre_ping=True
    )


def test_connection():

    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DATABASE(), VERSION()")
        )

        database, version = result.fetchone()

        print("MySQL connection successful!")
        print("Database:", database)
        print("MySQL version:", version)


if __name__ == "__main__":
    test_connection()
