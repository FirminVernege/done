from fastapi import status, HTTPException, Depends, APIRouter

from app import oauth2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users", tags=["Users"]
)


@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    # user_query = db.query(models.User).filter(
    #     models.User.email == new_user.email).first()

    # if user_query == None:

    #     db.add(new_user)

    #     db.commit()

    #     db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with an id of {id} was not found")

    return user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with an id of {id} was not found")

    if user.id == current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Cannot delete user. Administrative function only")

    user_query.delete(synchronize_session=False)

    db.commit()
