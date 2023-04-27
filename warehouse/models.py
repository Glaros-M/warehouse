from warehouse.exeptions import ItemNotFoundError, DeficitStockError


class Technic:
    def __init__(self,
                 inventory_number: str,
                 made_in: str,
                 cost: float,
                 model: str,
                 id: int | None = None):
        self.inventory_number = inventory_number
        self.made_in = made_in
        self.cost = cost
        self.model = model
        if id:
            self.id = id


class Employee:
    def __init__(self,
                 name: str,
                 surname: str,
                 patronimic: str,
                 login: str,
                 hased_password: str,
                 id: int | None = None
                 ):
        if id:
            self.id = id
        name = name
        surname = surname
        patronimic = patronimic
        login = login
        hased_password = hased_password


class StoreItemMixin:
    def store_item(self, item: Technic, count: int):
        if item not in self.items:
            self.items.update({item: count})
        else:
            self.items[item] = self.items[item] + count

    def take_item(self, item: Technic, quantity: int):
        if item not in self.items:
            raise ItemNotFoundError
        else:
            if self.items[item] < quantity:
                raise DeficitStockError
            self.items[item] = self.items[item] - quantity


class Warehouse(StoreItemMixin):
    def __init__(self,
                 address: str,
                 employee: Employee,
                 id: int | None = None,
                 items: dict | None = None):
        if id:
            self.id = id
        if not items:
            items = {}
        self.items = items
        self.address = address
        self.employee = employee


class Invoice(StoreItemMixin):
    def __init__(self,
                 is_receiving: bool,
                 from_who: str | Employee,
                 to: str | Employee,
                 id: int | None = None,
                 items: dict | None = None
                 ):
        if id:
            self.id = id
        if not items:
            items = {}
        self.items = items
        self.is_receiving = is_receiving
        self.from_who = from_who
        self.to = to
