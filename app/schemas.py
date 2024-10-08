from typing import Literal, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint


class VehicleBase(BaseModel):
    numberplate: str
    color: str
    price: float
    rented: bool = False


class VehicleCreate(VehicleBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class VehicleRental(VehicleBase):
    id: int


class Vehicle(VehicleBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


class VehicleOut(BaseModel):
    Vehicle: Vehicle
    rentals: int

    class Config:
        orm_mode: True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class RentalCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    vehicle_id: int
    customer_id: int
    calendar_color: str
    dir: Literal[0, 1]


class CustomerBase(BaseModel):
    name: str
    address: str
    license_number: str
    date_of_birth: str
    license_expiration_date: str


class Customer(CustomerBase):
    id: int
    created_at: datetime
    created_by: int


class CustomerOut(Customer):
    id: int
    created_at: datetime

    class Config:
        from_attributes: True


class RentalOut(BaseModel):
    start_date: datetime
    end_date: datetime
    calendar_color: str
    customer: CustomerOut
    vehicle: VehicleRental

    class Config:
        from_attributes = True


class CustomerCreate(CustomerBase):
    pass


class SaleBase(BaseModel):
    vehicle_id: int
    discount: float
    price: float


class SaleCreate(SaleBase):
    pass
