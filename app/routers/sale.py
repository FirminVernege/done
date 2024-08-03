from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def sale(sale: schemas.SaleCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.id == sale.vehicle_id).filter(models.Vehicle.owner_id == current_user.id).first()

    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with an id of {sale.vehicle_id} does not exist")

    new_sale = models.Sale(owner_id=current_user.id, **sale.model_dump())

    db.add(new_sale)

    db.commit()

    db.refresh(new_sale)

    return new_sale
