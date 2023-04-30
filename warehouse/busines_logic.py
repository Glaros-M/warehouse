from sqlalchemy.orm import Session
from sqlalchemy import Select
from db import engine
import models
from normal_distribution import get_nd
from random import choices


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
    for j in range(100):
        i, p = choices([(i1, nd[0]), (i2, nd[1]), (i3, nd[2]), (i4, nd[3]), (i5, nd[4])], weights=nd)[0]

        inv_num = f"№ ОВТ {j}"
        model = f"Изделие {j}.{p}"
        t1 = models.Technic(inventory_number=inv_num, made_in="Ru", cost=p, model=model)

        inv_item = models.InvoiceItems(quantity=1)
        inv_item.technic = t1

        i.items.append(inv_item)

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


def get_remains_for_warehouse(warehouse_id: int, *, session: Session) -> tuple[
    models.Warehouse | None, list[models.Technic]]:
    w = session.get(models.Warehouse, warehouse_id)
    inp: list[models.Invoice] = [x for x in w.invoices if x.is_receiving]
    out: list[models.Invoice] = [x for x in w.invoices if not x.is_receiving]

    inp_set = set()
    for inv in inp:
        for t in inv.technic:
            inp_set.add(t)

    out_set = set()
    for inv in out:
        for t in inv.technic:
            out_set.add(t)

    result = inp_set - out_set
    return w, list(result)


def get_remains_for_all_warehouse(*, session: Session):
    warehouses = list(session.execute(Select(models.Warehouse.id)).scalars())
    remains_w = []
    for w_id in warehouses:
        remains_w.append(get_remains_for_warehouse(w_id, session=session))

    return remains_w


if __name__ == '__main__':
    s = Session(engine)
    models.Base.metadata.create_all(engine)
    upload_100_technic()

    #w_r = get_remains_for_all_warehouse(session=s)
    #for w, r in w_r:
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
