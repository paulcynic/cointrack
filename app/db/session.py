from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from postgresql import psycopg2
# engine = create_engine('postgresql+psycopg2://pg_user:pq_password@localhost:5432/mydatabase')

SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # required for sqlite
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

