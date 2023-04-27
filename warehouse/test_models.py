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
        id = t2._id


T = models.Technic(id=0,
                   inventory_number="ОВТ1010432124",
                   made_in="USSR",
                   cost=123.45,
                   model="zenith camera"
                   )


def test_stored_items():
    si = models.StoredItem(item=T, count=1)


def test_warehouse_create():
    w1 = models.Warehouse(id=0,
                          address="Патриотов проспект, д.17")
    w2 = models.Warehouse(address="Патриотов проспект, д.17")
    with pytest.raises(AttributeError):
        id = w2._id


def test_warehouse_items():
    si = models.StoredItem(item=T, count=1)
    w = models.Warehouse(id=0,
                         address="Патриотов проспект, д.17", items=[si])

    assert w.items == [si]
    w.add_item(si)
    assert w.items == [si]
    assert w.get_item(si).count == 2
