from sqlalchemy import ForeignKey, BigInteger, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from normal_distribution import get_nd
from random import choices

from db import engine


class Base(DeclarativeBase):
    pass


class Technic(Base):
    __tablename__ = "technic"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    inventory_number: Mapped[str]
    made_in: Mapped[str]
    cost: Mapped[float]
    model: Mapped[str]

    def __repr__(self):
        return f"{self.id=} {self.inventory_number=} {self.made_in=} {self.cost=} {self.model=}"


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronimic: Mapped[str]
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    warehouse = relationship("Warehouse", back_populates="employee")

    def __repr__(self):
        return f"{self.surname} {self.name} {self.patronimic}"


class Warehouse(Base):
    __tablename__ = "warehouse"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    address: Mapped[str]
    employee = relationship("Employee", back_populates="warehouse", uselist=False)
    invoices: Mapped[list["Invoice"]] = relationship("Invoice")

    def __repr__(self):
        return f"{self.id=} {self.address=} {self.employee=}"

"""
invoice_items = Table(
    "invoice_items",
    Base.metadata,
    Column("invoice_id", ForeignKey("invoice.id")),
    Column("technic_id", ForeignKey("technic.id")),
)"""


class InvoiceItems(Base):
    __tablename__ = "invoice_items"
    invoice_id = Column(ForeignKey("invoice.id"), primary_key=True)
    technic_id = Column(ForeignKey("technic.id"), primary_key=True)
    quantity: Mapped[int]
    technic: Mapped[Technic] = relationship("Technic")

    def __repr__(self):
        return f"{self.quantity=}  {self.technic}"


class Invoice(Base):
    __tablename__ = "invoice"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    is_receiving: Mapped[bool]
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    items: Mapped[list[InvoiceItems]] = relationship("InvoiceItems")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
