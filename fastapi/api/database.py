# Using SQLAlchemy ORM

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQL_ALCHEMY_DATABASE_URL = 'sqlite:///workout_app.db'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={
                       'check_same_thread': False})

# Create a session class.  autocommit and autoflush are set to False.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models.
Base = declarative_base()
