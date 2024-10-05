from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/customer",
    tags=["Customers"]
)


@router.get("/")
def get_customers(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customers = db.query(models.Customer).filter(
        models.Customer.created_by == current_user.id).all()

    return customers


@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    customer = models.Customer(
        created_by=current_user.id, **customer.model_dump())

    db.add(customer)

    db.commit()

    db.refresh(customer)

    return (customer)


@router.get("/{id}")
def get_customer(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    customer = db.query(models.Customer).filter(
        models.Customer.created_by == current_user.id).filter(models.Customer.id == id).first()

    if not customer:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer with an id of {id} was not found")
    return customer


@router.delete("/{id}")
def get_customer(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    customer_query = db.query(models.Customer).filter(
        models.Customer.created_by == current_user.id).filter(models.Customer.id == id)

    customer = customer_query.first()

    if customer == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with an id of {id} does not exist")

    if customer.created_by != customer.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    customer_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
