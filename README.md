## Setup

1. `pip install poetry`
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. Enter into database:
    psql -h localhost -U username -d your_db
    Create database 'your_db'; 
4. Check and update your database config in 
    ./app/db/session.py
        (SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pg_username:pg_password@localhost:5432/your_db')
5. Remove all files from the directory ./alembic/versions/
6. Run the Database via poetry `poetry run ./prestart.sh`
7. Check manually your database if all tables were created.
8. Run the FastAPI server via poetry `poetry run ./run.sh`
9. Open http://localhost:8002/
