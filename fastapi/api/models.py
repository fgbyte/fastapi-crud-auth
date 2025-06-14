from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Define the association table for the many-to-many relationship between Workouts and Routines
workout_routine_association = Table(
    'workout_routine', Base.metadata,
    # Foreign key to the Workouts table
    Column('workout_id', Integer, ForeignKey('workouts.id')),
    # Foreign key to the Routines table
    Column('routine_id', Integer, ForeignKey('routines.id'))
)


class User(Base):
    __tablename__ = 'users'
    # Unique identifier for the user
    id = Column(Integer, primary_key=True, index=True)
    # Username of the user, must be unique
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # Hashed password for the user


class Workout(Base):
    __tablename__ = 'workouts'
    # Unique identifier for the workout
    id = Column(Integer, primary_key=True, index=True)
    # Foreign key to the Users table
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)  # Name of the workout
    description = Column(String, index=True)  # Description of the workout
    routines = relationship(
        'Routine', secondary=workout_routine_association, back_populates='workouts')  # Relationship to Routines, using the association table


class Routine(Base):
    __tablename__ = 'routines'
    # Unique identifier for the routine
    id = Column(Integer, primary_key=True, index=True)
    # Foreign key to the Users table
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)  # Name of the routine
    description = Column(String, index=True)  # Description of the routine
    workouts = relationship(
        'Workout', secondary=workout_routine_association, back_populates='routines')  # Relationship to Workouts, using the association table


Workout.routines = relationship(  # Redefine the relationship to work around a circular import
    'Routine', secondary=workout_routine_association, back_populates='workouts')
