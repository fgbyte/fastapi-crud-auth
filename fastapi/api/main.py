from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import auth

app = FastAPI()

# add this for creating the tables in the database
Base.metadata.create_all(bind=engine)


# Add a middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['https://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# include the router to the app
app.include_router(auth.router)
