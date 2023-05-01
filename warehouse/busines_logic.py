import random

from sqlalchemy.orm import Session
from sqlalchemy import Select
from db import engine
import models
from normal_distribution import get_nd
from random import choices

from matplotlib import pyplot as plt


def upload_100_technic():
    e1 = models.Employee(surname="Иванов", name="Иван", patronimic="Иванович")
    e2 = models.Employee(surname="Петров", name="Петр", patronimic="Петрович")
    e3 = models.Employee(surname="Николаев", name="Николай", patronimic="Николаевич")
    e4 = models.Employee(surname="Сергеев", name="Сергей", patronimic="Сергеевич")
    e5 = models.Employee(surname="Александров", name="Александр", patronimic="Александрович")

    w1 = models.Warehouse(address="г. Воронеж, ул. Докучаева, д.1", employee=e1)
    w2 = models.Warehouse(address="г. Воронеж, ул. Докучаева, д.2", employee=e2)
    w3 = models.Warehouse(address="г. Воронеж, ул. Докучаева, д.3", employee=e3)
    w4 = models.Warehouse(address="г. Воронеж, ул. Докучаева, д.4", employee=e4)
    w5 = models.Warehouse(address="г. Воронеж, ул. Докучаева, д.5", employee=e5)

    i1 = models.Invoice(is_receiving=True)
    i2 = models.Invoice(is_receiving=True)
    i3 = models.Invoice(is_receiving=True)
    i4 = models.Invoice(is_receiving=True)
    i5 = models.Invoice(is_receiving=True)

    nd = get_nd(5, 0.8)  # [2.19, 22.83, 49.87, 22.83, 2.19]
    number_of_items = 100
    invoices = [i1, i2, i3, i4, i5]
    for j in range(number_of_items):
        inv_num = f"№ ОВТ {j}"
        model = f"Изделие 00x{j}"
        cost = round(1000 / random.randint(1, 100), 2)
        t1 = models.Technic(inventory_number=inv_num, made_in="Ru", cost=cost, model=model)
        print(t1.cost)
        quantity_of_item = random.randint(0, 100)
        qs = [0 for _ in range(5)]
        for _ in range(quantity_of_item):
            q = choices(range(5), weights=nd)[0]
            qs[q] += 1

        for i in range(len(invoices)):
            if qs[i] > 0:
                inv_item = models.InvoiceItems(quantity=qs[i])
                inv_item.technic = t1
                invoices[i].items.append(inv_item)

    w1.invoices.append(i1)
    w2.invoices.append(i2)
    w3.invoices.append(i3)
    w4.invoices.append(i4)
    w5.invoices.append(i5)

    session = Session(engine)

    session.add(w1)
    session.add(w2)
    session.add(w3)
    session.add(w4)
    session.add(w5)
    session.commit()

    print(w1.id)
    print(w1.invoices[0].items)
    print(len(w1.invoices[0].items))
    session.close()


def get_remains_for_warehouse(warehouse_id: int, *, session: Session) -> tuple[models.Warehouse | None, dict]:
    w = session.get(models.Warehouse, warehouse_id)
    inp: list[models.Invoice] = [x for x in w.invoices if x.is_receiving]
    out: list[models.Invoice] = [x for x in w.invoices if not x.is_receiving]

    warehouse_items_dict = {}
    for inv in inp:
        for item in inv.items:
            if item not in warehouse_items_dict:
                warehouse_items_dict.update({item.technic: item.quantity})
            else:
                quantity = warehouse_items_dict[item.technic] + item.quantity
                warehouse_items_dict.update({item.technic: quantity})

    for inv in out:
        for item in inv.items:
            if item not in warehouse_items_dict:
                pass  # RAISE ERROR!!!! ЭТО ЗНАЧИТ ЧТО ЗАФИКСИРОВАНА НАКЛАДНАЯ НА СПИСАНИЕ ТОВАРА КОТОРОГО НЕТ НА СКЛАДЕ
            else:
                quantity = warehouse_items_dict[item.technic] - item.quantity
                if quantity < 0:
                    pass  # RAISE ERROR!!!! НЕВОЗМОЖНАЯ СИТУАЦИЯ, списано со склада больше чем там есть
                elif quantity == 0:
                    del warehouse_items_dict[item.technic]
                else:
                    warehouse_items_dict.update({item.technic: quantity})

    return w, warehouse_items_dict


def get_remains_for_all_warehouse(*, session: Session):
    warehouses = list(session.execute(Select(models.Warehouse.id)).scalars())
    remains_w = []
    for w_id in warehouses:
        remains_w.append(get_remains_for_warehouse(w_id, session=session))

    return remains_w


def get_remains_for_technic_in_warehouse(technic_id: int, *, session: Session) -> tuple[models.Technic | None, dict]:
    technic = session.get(models.Technic, technic_id)
    stmt = Select(models.Technic.id,
                  models.Invoice.is_receiving,
                  models.InvoiceItems.quantity,
                  models.Invoice.warehouse_id
                  ) \
        .join(models.InvoiceItems, models.Technic.id == models.InvoiceItems.technic_id) \
        .join(models.Invoice, models.Invoice.id == models.InvoiceItems.invoice_id) \
        .where(models.Technic.id == technic_id)

    a = session.execute(stmt)

    warehouse_dict = {}
    for _, is_receiving, quantity, warehouse_id in a:
        if warehouse_id not in warehouse_dict:
            warehouse_dict.update({warehouse_id: quantity})
        else:
            if not is_receiving:
                quantity = -quantity
            quantity = warehouse_dict[warehouse_id] + quantity
            warehouse_dict.update({warehouse_id: quantity})

    return technic, warehouse_dict


def get_remains_for_technic(technic_id, *, session: Session) -> int:
    stmt = Select(models.Technic.cost,
                  models.Invoice.is_receiving,
                  models.InvoiceItems.quantity
                  ) \
        .join(models.InvoiceItems, models.Technic.id == models.InvoiceItems.technic_id) \
        .join(models.Invoice, models.Invoice.id == models.InvoiceItems.invoice_id) \
        .where(models.Technic.id == technic_id)
    a = session.execute(stmt)

    count = 0
    for cost, is_receiving, quantity in a:
        # print(cost, is_receiving, quantity)
        if not is_receiving:
            quantity = -quantity
        count += quantity
    return count


def get_all_remains_for_technics(*, session: Session):
    stmt = Select(models.Technic.id)
    ids = list(session.execute(stmt).scalars())
    all_remains = {}
    for id in ids:
        technic = session.get(models.Technic, id)
        quantity = get_remains_for_technic(id, session=session)
        all_remains.update({technic: quantity})
    return all_remains


def get_diagram(*, session: Session):
    remains = get_all_remains_for_technics(session=session)
    lst = [quantity for _, quantity in remains.items()]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(lst, bins=len(lst))

    plt.show()


if __name__ == '__main__':
    s = Session(engine)
    #upload_100_technic()
    # get_remains_for_warehouse(1, session=s)
    # get_remains_for_technic(1, session=s)
    # get_all_remains_for_technics(session=s)
    # get_remains_for_technic(1, session=s)
    # print(get_remains_for_technic_in_warehouse(1, session=s))
    get_diagram(session=s)

    # w_r = get_remains_for_all_warehouse(session=s)
    # for w, r in w_r:
    #    print(w, len(r))

    """
    # Тест добавление накладной на списание
    get_remains_for_warehouse(2, session=s)

    t = s.get(models.Technic, 7)

    i1 = models.Invoice(is_receiving=False, technic=[t])
    w = s.get(models.Warehouse, 2)
    w.invoices.append(i1)
    s.commit()
    get_remains_for_warehouse(2, session=s)"""
