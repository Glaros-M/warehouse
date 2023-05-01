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
    warehouses = [w1, w2, w3, w4, w5]

    i1 = models.Invoice(is_receiving=True)
    i2 = models.Invoice(is_receiving=True)
    i3 = models.Invoice(is_receiving=True)
    i4 = models.Invoice(is_receiving=True)
    i5 = models.Invoice(is_receiving=True)
    invoices = [i1, i2, i3, i4, i5]

    number_of_items = 100
    nd = get_nd(100, 15)  # [2.19, 22.83, 49.87, 22.83, 2.19]

    technics = []
    for j in range(number_of_items):
        inv_num = f"№ ОВТ {j}"
        model = f"Изделие 00x{j}"
        cost = round(1000 / random.randint(1, 100), 2)
        t1 = models.Technic(inventory_number=inv_num, made_in="Ru", cost=cost, model=model)
        technics.append(t1)


    for i in range(number_of_items):
        q = random.choices([x for x in range(100)], weights=nd)[0]
        inv_item = models.InvoiceItems(quantity=q)
        inv_item.technic = technics[i]
        j = random.randint(0, 4)
        invoices[j].items.append(inv_item)
    """
    n_item = [x for x in range(number_of_items)]
    n_quantity = [0 for _ in range(number_of_items)]
    while True:
        i = random.choices(n_item, weights=nd)[0]
        n_quantity[i] += 1
        if max(n_quantity) >=100:
            break

    for i in range(number_of_items):
        if n_quantity[i] > -1:
            inv_item = models.InvoiceItems(quantity=n_quantity[i])
            inv_item.technic = technics[i]
            j = random.randint(0, 4)
            invoices[j].items.append(inv_item)
    """
    session = Session(engine)
    for i in range(5):
        warehouses[i].invoices.append(invoices[i])
        session.add(warehouses[i])

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

    plt.savefig('static\\1.jpg')


if __name__ == '__main__':
    #models.Base.metadata.create_all(engine)
    s = Session(engine)
    #upload_100_technic()

    #get_diagram(session=s)
