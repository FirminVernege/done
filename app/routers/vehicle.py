
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.get("/", response_model=List[schemas.VehicleOut])
def get_vehicles(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = "", rented: Optional[bool] = False):

    vehicles = db.query(models.Vehicle, func.count(models.Rental.vehicle_id).label("rentals")).join(
        models.Rental, models.Rental.vehicle_id == models.Vehicle.id, isouter=True).group_by(models.Vehicle.id).filter(
        models.Vehicle.owner_id == current_user.id).filter(models.Vehicle.numberplate.contains(search)).filter(models.Vehicle.rented == rented).limit(limit).offset(skip).all()
    vehicles = list(map(lambda x: x._mapping, vehicles))

    return vehicles


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_vehicle = models.Vehicle(
        owner_id=current_user.id,  **vehicle.model_dump())

    db.add(new_vehicle)

    db.commit()

    db.refresh(new_vehicle)

    return new_vehicle


@router.get("/{id}", response_model=schemas.VehicleOut)
def get_vehicle(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle = db.query(models.Vehicle, func.count(models.Rental.vehicle_id).label("rentals")).join(
        models.Rental, models.Rental.vehicle_id == models.Vehicle.id, isouter=True).group_by(models.Vehicle.id).filter(models.Vehicle.id == id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with an id of {id} was not found")

    vehicle = vehicle._mapping

    if vehicle.get("Vehicle").owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")

    return vehicle


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    vehicle = vehicle_query.first()

    if vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with an id of {id} does not exist")

    if vehicle.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")

    vehicle_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_vehicle(id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.id == id)

    updated_vehicle = vehicle_query.first()
    if updated_vehicle == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with an id of {id} does not exist")

    if updated_vehicle.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action.")
    vehicle_query.update(vehicle.model_dump(), synchronize_session=False)

    db.commit()

    return vehicle_query.first()
