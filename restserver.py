from flask import Flask, jsonify, request
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
    with open('mytransactions.json','r') as f:
        data = json.load(f)
        for each_transaction in data:
            query_maker.add_transaction(each_transaction['credit'], each_transaction['date'], each_transaction['uuid'],
                                        each_transaction['store'])
    with open('mystores.json','r') as f:
        data = json.load(f)
        for each_store in data:
            query_maker.add_store(each_store['name'])
    return 'added'

@app.route('/stores',methods=["GET"])
def stores_list():
    stores = query_maker.get_stores()
    list = []
    for each in stores:
        list.append(each[0])
    print(list)
    return jsonify(list)

@app.route('/createcategory',methods=["POST"])
def create_category():
    category = request.args.get('category')
    if query_maker.category_exists(category):
        return "This category already exists"
    else:
        query_maker.create_category



if __name__ == '__main__':
    app.run()
