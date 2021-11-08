from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://paulcynic@localhost/cointrack_db', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

