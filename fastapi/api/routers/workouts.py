from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, status

# Load the Model
from api.models import Workout
# Load the Deps
from api.deps import db_dependency, user_dependency


# Add the route
router = APIRouter(
    prefix='/workouts',
    tags=['workouts']
)


# Pydantic Schema for Workout route 👇
class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None


class WorkoutCreate(WorkoutBase):
    # `pass` it's a syntactically required statement to have an empty class body.
    pass


# Workout Endpoints 👇
@router.get('/')
def get_workout(db: db_dependency, user: user_dependency, workout_id: int):
    return db.query(Workout).filter(Workout.id == workout_id).first()


@router.get('/workouts')
def get_workouts(db: db_dependency, user: user_dependency):
    return db.query(Workout).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_workout(db: db_dependency, user: user_dependency, workout: WorkoutCreate):
    db_workout = Workout(**workout.model_dump(), user_id=user.get('id'))
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete('/')
def delete_workout(db: db_dependency, user: user_dependency, workout_id: int):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout:
        db.delete(db_workout)
        db.commit()
    return db_workout
