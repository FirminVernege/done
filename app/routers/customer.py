from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/customer",
    tags=["Customers"]
)


@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customer = models.Customer(
        created_by=current_user.id, **customer.model_dump())

    db.add(customer)

    db.commit()

    db.refresh(customer)

    return (customer)
