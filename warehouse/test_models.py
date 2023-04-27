from warehouse import models
from warehouse.exeptions import ItemNotFoundError, DeficitStockError
import pytest


def test_technic_create():
    t1 = models.Technic(id=0,
                        inventory_number="ОВТ1010432124",
                        made_in="USSR",
                        cost=123.45,
                        model="zenith camera"
                        )

    t2 = models.Technic(inventory_number="ОВТ1010432124",
                        made_in="USSR",
                        cost=123.45,
                        model="zenith camera"
                        )
    with pytest.raises(AttributeError):
        id = t2.id


T = models.Technic(id=0,
                   inventory_number="ОВТ1010432124",
                   made_in="USSR",
                   cost=123.45,
                   model="zenith camera"
                   )

T2 = models.Technic(id=1,
                    inventory_number="ОВТ1010432124",
                    made_in="USSR",
                    cost=123.45,
                    model="zenith camera"
                    )



def test_employee_create():
    e = models.Employee(
        id=0,
        name="",
        surname="",
        patronimic="",
        login="",
        hased_password=""
    )


E = models.Employee(
    id=0,
    name="",
    surname="",
    patronimic="",
    login="",
    hased_password=""
)


def test_warehouse_create():
    w1 = models.Warehouse(id=0,
                          address="Патриотов проспект, д.17", employee=E)
    w2 = models.Warehouse(address="Патриотов проспект, д.17", employee=E)
    with pytest.raises(AttributeError):
        id = w2.id


def test_invoice_create():
    inv = models.Invoice(id=0,
                         is_receiving=True,
                         from_who="Какой то поставшик, ООО \"ООО\"",
                         to=E
                         )


def test_warehouse_items():
    w = models.Warehouse(address="Патриотов проспект, д.1", employee=E)
    assert w.items == {}
    w.store_item(T, 10)
    assert w.items[T] == 10

    w.store_item(T, 20)
    assert w.items[T] == 30

    w.take_item(T, 15)
    assert w.items[T] == 15

    with pytest.raises(ItemNotFoundError):
        w.take_item(T2, 10)

    with pytest.raises(DeficitStockError):
        w.take_item(T, 999999)


def test_invoice_items():
    inv = models.Invoice(id=0,
                         is_receiving=True,
                         from_who="Какой то поставшик, ООО \"ООО\"",
                         to=E
                         )
    assert inv.items == {}
    inv.store_item(T, 10)
    assert inv.items[T] == 10

    inv.store_item(T, 20)
    assert inv.items[T] == 30

    inv.take_item(T, 15)
    assert inv.items[T] == 15

    with pytest.raises(ItemNotFoundError):
        inv.take_item(T2, 10)

    with pytest.raises(DeficitStockError):
        inv.take_item(T, 999999)
