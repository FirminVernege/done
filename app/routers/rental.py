from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/rental", tags=["Rentals"]
)


@router.get("/", response_model=List[schemas.RentalOut])
def get_rentals(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    rentals = db.query(models.Rental).filter(
        models.Rental.user_id == current_user.id).all()

    return rentals


@router.post("/", status_code=status.HTTP_201_CREATED)
def rental(rental: schemas.RentalCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == rental.vehicle_id).filter().first()

    customer = db.query(models.Customer).filter(models.Customer.id == rental.customer_id).filter(
    ).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with an id of {
                            rental.customer_id} doesn't exist")

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id of {rental.vehicle_id} doesn't exist")

    rental_query = db.query(models.Rental).filter(
        models.Rental.user_id == current_user.id).filter(models.Rental.vehicle_id == rental.vehicle_id, models.Rental.user_id == current_user.id)

    found_rental = rental_query.first()

    if (rental.dir == 1):
        if found_rental:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Vehicle with number plate {
                                vehicle.numberplate} has already been rented")

        new_rental = models.Rental(
            vehicle_id=rental.vehicle_id, user_id=current_user.id, customer_id=rental.customer_id, calendar_color=rental.calendar_color)

        db.add(new_rental)

        db.commit()

        return {"message": "Successfully rented vehicle"}
    else:
        if not found_rental:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Rental does not exist")

        rental_query.delete(synchronize_session=False)

        db.commit()

        return {"message": "Successfully deleted rental"}
