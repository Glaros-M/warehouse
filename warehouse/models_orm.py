from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey, BigInteger, Integer, String, Table, Column
from sqlalchemy.orm import DeclarativeBase
from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from normal_distribution import get_nd
from random import choices

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

    e1 = Employee(surname="Иванов", name="Иван", patronimic="Иванович")
    e2 = Employee(surname="Петров", name="Петр", patronimic="Петрович")
    e3 = Employee(surname="Николаев", name="Николай", patronimic="Николаевич")
    e4 = Employee(surname="Сергеев", name="Сергей", patronimic="Сергеевич")
    e5 = Employee(surname="Александров", name="Александр", patronimic="Александрович")

    w1 = Warehouse(address="г. Воронеж, ул. Докучаева, д.1", employee=e1)
    w2 = Warehouse(address="г. Воронеж, ул. Докучаева, д.2", employee=e2)
    w3 = Warehouse(address="г. Воронеж, ул. Докучаева, д.3", employee=e3)
    w4 = Warehouse(address="г. Воронеж, ул. Докучаева, д.4", employee=e4)
    w5 = Warehouse(address="г. Воронеж, ул. Докучаева, д.5", employee=e5)

    i1 = Invoice(is_receiving=True, technic=[])
    i2 = Invoice(is_receiving=True, technic=[])
    i3 = Invoice(is_receiving=True, technic=[])
    i4 = Invoice(is_receiving=True, technic=[])
    i5 = Invoice(is_receiving=True, technic=[])

    nd = get_nd(5, 0.8, to_int=True)  # [2.19, 22.83, 49.87, 22.83, 2.19]
    for j in range(100):
        t1 = Technic(inventory_number=str(j), made_in="Ru", cost=100.00, model="1")
        i = choices([i1, i2, i3, i4, i5], weights=nd)[0]
        i.technic.append(t1)


    w1 = Warehouse(address="", employee=e1, invoices=[i3])

    session = Session(engine)

    session.add(w1)
    session.commit()
    print(w1.id)
    print(w1.invoices[0].technic)
    print(len(w1.invoices[0].technic))
