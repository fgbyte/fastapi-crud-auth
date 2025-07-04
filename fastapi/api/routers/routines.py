from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter, status
from sqlalchemy.orm import joinedload

# Load the Model
from api.models import Routine, Workout
# Load the Deps
from api.deps import db_dependency, user_dependency

# Add the route prefix
router = APIRouter(
    prefix='/routines',
    tags=['routines']
)


# Create the Pydantic model
class RoutineBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoutineCreate(RoutineBase):
    workouts: List[int] = []


# Routines Endpoints
@router.get('/')
def get_routine(db: db_dependency, user: user_dependency):
    return db.query(Routine).options(joinedload(Routine.workouts)).filter(Routine.user_id == user.get('id')).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_routine(db: db_dependency, user: user_dependency, routine: RoutineCreate):
    db_routine = Routine(
        name=routine.name, description=routine.description, user_id=user.get('id'))
    for workout_id in routine.workouts:
        workout = db.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            db_routine.workouts.append(workout)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    db_routines = db.query(Routine).options(joinedload(
        Routine.workouts)).filter(Routine.id == db_routine.id).first()
    return db_routines


@router.delete('/')
def delete_routine(db: db_dependency, user: user_dependency, routine_id: int):
    db_routine = db.query(Routine).filter(Routine.id == routine_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
    return db_routine
