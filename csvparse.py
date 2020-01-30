import uuid
from html.parser import HTMLParser
import json


class Transaction:
    def __init__(self, date, store, credit, balance, debit, amount):
        self.date = date
        self.store = store
        self.debit = debit
        self.credit = credit
        self.amount = amount
        self.balance = balance

    def __str__(self):
        return "This transaction is " + self.date + " " + self.store + " " + self.credit + " " + " "


class Store:
    def __init__(self, name, spent):
        self.name = name
        self.spent = spent
        self.transactions = []

    def add_purchase(self, amount, uid):
        self.spent += amount
        self.transactions.append(uuid)


def check_row_class(attr):
    for each in attr:
        if each[0] == 'class':
            if str(each[1]).__contains__('transaction-row'):
                return extract_date(attr)
    return None


def extract_date(attributes):
    for each in attributes:
        if each[0] == 'id':
            date = str(each[1])
            return date
    return None


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inside_table_body = False
        self.inside_transaction_row = False
        self.current_column = 0
        self.date_column = True
        self.current_transaction = None
        self.transactions = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self.inside_table_body = True
        if self.inside_table_body:
            if tag == 'tr':
                date = check_row_class(attrs)
                if date is not None:
                    self.current_transaction = Transaction(date, 0, 0, 0, 0, 0)
                    self.inside_transaction_row = True
        if self.inside_transaction_row:
            if tag == 'td':
                self.current_column = self.current_column + 1
                self.date_column = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.inside_transaction_row:
                self.inside_transaction_row = False
                self.date_column = False
                self.current_column = 0
                self.transactions.append(self.current_transaction.__dict__)
                self.current_transaction = None

    def handle_data(self, data):
        if self.date_column:
            data = str(data).strip()

            # if self.current_column == 1:
            #         self.current_transaction = Transaction(data, 0, 0, 0, 0, 0)
            if self.current_column == 2:
                self.current_transaction.store = data
            if self.current_column == 3:
                self.current_transaction.debit = data
            if self.current_column == 4:
                self.current_transaction.credit = data
            if self.current_column == 5:
                self.current_transaction.balance = data
                print(self.current_transaction)
        self.date_column = False


def main():
    filename = './table.html'
    f = open(filename, "r").read()
    parser = MyHTMLParser()
    parser.feed(f)
    with open('mytransactions.json', 'w') as f:
        json.dump(parser.transactions, f)

if __name__ == "__main__":
    main()
