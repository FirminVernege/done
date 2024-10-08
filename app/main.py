from fastapi import Depends, FastAPI

from app import oauth2
from . import models
from .routers import vehicle, user, auth, rental, customer, sale
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
# from .database import engine
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
app.include_router(customer.router)
app.include_router(sale.router)


@app.get("/")
def root(current_user: int = Depends(oauth2.get_current_user)):
    return {"message": "Hello World"}
