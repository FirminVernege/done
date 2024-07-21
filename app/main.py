from fastapi import FastAPI
from . import models
# from .database import engine
from .routers import vehicle, user, auth, rental
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

# models.Base.metadata.create_all(bind=engine)
# replaced with alembic


app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vehicle.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(rental.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
