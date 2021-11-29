from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://paulcynic@localhost/cointrack_db'

engine = create_engine(SQLALCHEMY_DATABASE_URI)


# if you want to use sqlite3 database:
# SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URI,
#     # required for sqlite
#     connect_args={"check_same_thread": False},
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

