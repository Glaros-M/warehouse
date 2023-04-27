from warehouse import models
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


def test_stored_items_create():
    si = models.StoredItem(item=T, count=1)


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
    assert w.items == []
    si = models.StoredItem(T, 1)
    si2 = models.StoredItem(T, 10)
    w.add_item(si)
    assert si in w.items
    assert len(w.items) == 1
    w.add_item(si)
    assert len(w.items) == 1
    w.add_item(si2)
    assert len(w.items) == 1
