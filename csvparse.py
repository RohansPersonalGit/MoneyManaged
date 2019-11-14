import csv
import uuid


class Transaction:
    def __init__(self, date, store, amount, balance):
        self.date = date
        self.store = store
        self.amount = amount
        self.balance = balance
        self.uuid = uuid.uuid1()

    def name(self):
        return self.name


class Store:
    def __init__(self, name, spent):
        self.name = name
        self.spent = spent
        self.transactions = []

    def add_purchase(self, amount, uid):
        self.spent += amount
        self.transactions.append(uuid)


transaction_list = []
store_list = {}


def update(name, amount, uid):
    store = store_list.get(name, None)
    if store is None:
        store = Store(name, 3)
        store_list[name] = store
    store.add_purchase(float(amount), uid)

def main():
    with open('accountactivity.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            print ','.join(row)
            t = Transaction(row[0], row[1], row[2], row[4])
            update(t.store, t.amount, t.uuid)
            transaction_list.append(t)


if __name__ == "__main__":
    main()
