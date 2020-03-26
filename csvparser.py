import csv
import uuid
from uuid import UUID
import os
import json
import re


class Transaction:
    def __init__(self, date, store, credit, debit, balance):
        self.date = date
        self.store = store
        self.debit = debit
        self.credit = credit
        self.balance = balance
        self.balance = balance
        self.uuid = uuid.uuid1()

    def name(self):
        return self.name

    def __str__(self):
        return "I happened on " + self.date + ' ' + self.debit


class Store:
    def __init__(self, name):
        self.name = name
        self.spent = 0
        self.transactions = []

    def add_purchase(self, amount, uid):
        self.spent += amount
        self.transactions.append(uid)

    def __str__(self):
        return "I am a store named " + self.name + "You have spent " + str(self.spent)


store_list = []


def update(name, amount, uid):
    found = False
    for each in store_list:
        if re.search('AMZN|Amazon', name) is not None:
            if each['name'] == 'Amazon':
                each['transactions'].append(name)
                each['spent'] += float(amount)
                found = True
                break
        elif each['name'] == name:
            each['spent'] += float(amount)
            each['transactions'].append(uid)
            found = True
            break
    if not found:
        if re.search('AMZN|Amazon', name) is not None:
            store = Store('Amazon')
            store.add_purchase(float(amount), name)
        else:
            if "'" in name:
                print('hit')
                name = name.replace("'", "''")
                print(name + " how")
            store = Store(name)
            store.add_purchase(float(amount), uid)
        store_list.append(store.__dict__)


def main():
    transaction_list = []
    for filename in os.listdir('./transactions'):
        if filename.endswith(".csv"):
            with open('./transactions/' + filename) as csvfile:
                reader = csv.DictReader(csvfile)
                spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in spamreader:
                    t = Transaction(row[0], row[1], row[2], row[3], row[4])
                    if row[2] != '':
                        update(t.store, t.credit, t.uuid)
                    transaction_list.append(t.__dict__)
    i = 0
    for each in transaction_list:
        print(each)
        i += 1
    print(i)
    for each in store_list:
        print(each)
    with open('mytransactions.json', 'w') as f:
        json.dump(transaction_list, f, cls=UUIDEncoder)
    with open('mystores.json', 'w') as f:
        json.dump(store_list, f, cls=UUIDEncoder)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    main()
