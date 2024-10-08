from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, nullable=False)
    numberplate = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=False)
    rented = Column(Boolean, server_default="FALSE", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    owner = Relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

# TODO: Remove default values for start and end date when app is created


class Rental(Base):
    __tablename__ = 'rentals'
    # TODO: Add id column back to rentals
    # id = Column(Integer, primary_key=True, nullable=False)

    start_date = Column(TIMESTAMP(timezone=True),
                        nullable=False, default=text('NOW()'))

    end_date = Column(TIMESTAMP(timezone=True),
                      nullable=False, default=text('NOW()'))

    calendar_color = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                     primary_key=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"),
                        primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey(
        "customers.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    customer = Relationship("Customer")

    vehicle = Relationship("Vehicle")

# Create a table to hold customer information


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    license_number = Column(String, nullable=False, unique=True)
    date_of_birth = Column(String, nullable=False)
    license_expiration_date = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    created_by = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)


class Sale(Base):
    __tablename__ = 'sales'
    # TODO: Add id back to sales table
    # id = Column(Integer, primary_key=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id", ondelete="CASCADE"),
                        primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    discount = Column(Float, nullable=False, default=0)
    price = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
