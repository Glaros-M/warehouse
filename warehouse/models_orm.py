from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, BigInteger, Integer, String, Table, Column

from sqlalchemy.orm import DeclarativeBase

from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from warehouse.exeptions import ItemNotFoundError, DeficitStockError

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)  # БД в оперативке


# engine_lite = create_engine("sqlite+pysqlite:///sqlite3.db", echo=False, max_overflow=100)  # БД в локальная sqlite
# engine = create_engine(CONNECTION_STRING, echo=False, max_overflow=100)


class Base(DeclarativeBase):
    pass


class Technic(Base):
    __tablename__ = "technic"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    inventory_number: Mapped[str]
    made_in: Mapped[str]
    cost: Mapped[float]
    model: Mapped[str]


class Employee(Base):
    __tablename__ = "employee"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    name: Mapped[str]
    surname: Mapped[str]
    patronimic: Mapped[str]
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    warehouse = relationship("Warehouse", back_populates="employee")


class Warehouse(Base):
    __tablename__ = "warehouse"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    address: Mapped[str]
    employee = relationship("Employee", back_populates="warehouse", uselist=False)
    invoices: Mapped[list["Invoice"]] = relationship("Invoice")


invoice_items = Table(
    "invoice_items",
    Base.metadata,
    Column("invoice_id", ForeignKey("invoice.id")),
    Column("technic_id", ForeignKey("technic.id")),
)


class Invoice(Base):
    __tablename__ = "invoice"
    id: Mapped[int] = mapped_column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True, autoincrement=True)
    is_receiving: Mapped[bool]
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    technic: Mapped[list[Technic]] = relationship("Technic", secondary=invoice_items)


if __name__ == '__main__':
    Base.metadata.create_all(engine)

    s = Session(engine)

    t1 = Technic(inventory_number="1", made_in="Ru", cost=100.00, model="1")
    e1 = Employee(name="", surname="", patronimic="")
    i1 = Invoice(is_receiving=True, technic=[t1])
    w1 = Warehouse(address="", employee=e1, invoices=[i1])


    session = Session(engine)

    session.add(t1)
    session.add(e1)
    session.add(i1)
    session.add(w1)
    session.commit()
    print(w1.id)
    print(w1.invoices[0].id)
