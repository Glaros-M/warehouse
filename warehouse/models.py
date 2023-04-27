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
            self._id = id


class StoredItem:
    def __init__(self, item: Technic, count: int):
        self.item = item
        self.count = count


class Warehouse:
    def __init__(self,
                 address: str,
                 id: int | None = None,
                 items: list[StoredItem] | None = None):
        if id:
            self._id = id
        if not items:
            items = []
        self.items = items
        self.address = address

    def add_item(self, item: StoredItem):
        if not item in self.items:
            self.items.append(item)
        else:
            self.items[self.items.index(item)].count += item.count

    def get_item(self, item: StoredItem) -> StoredItem:
        if item in self.items:
            return self.items[0]
