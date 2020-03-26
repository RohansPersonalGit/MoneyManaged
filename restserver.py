from flask import Flask
import os
import json
from Querymachine import Querymachine
app = Flask(__name__)
query_maker = Querymachine()
@app.route('/')
def main():
    return 'welcome to money managed'
@app.route('/reset')
def reset():
    query_maker.drop_tables()
    query_maker.create_tables()
    return 'reset this shit'

@app.route('/addtestinfo')
def add_info():
    # with open('mytransactions.json','r') as f:
    #     data = json.load(f)
    #     for each_transaction in data:
    #         query_maker.add_transaction(each_transaction['credit'], each_transaction['date'], each_transaction['uuid'])
    with open('mystores.json','r') as f:
        data = json.load(f)
        for each_store in data:
            query_maker.add_store(each_store['name'],each_store['spent'])
    return 'added'


if __name__ == '__main__':
    app.run()
