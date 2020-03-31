from flask import Flask, jsonify, request
from BackEnd.Querymachine import Querymachine
app = Flask(__name__)
query_maker = Querymachine()
import logging
# shitty server cant handle multiple client reqeusrts from one source yet rip
@app.before_request
def filter_prefetch():
    logging.debug("before request")
    logging.debug(request.headers)

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
    reset()
    with open('mytransactions.json', 'r') as f:
        data = json.load(f)
        for each_transaction in data:
            query_maker.add_transaction(each_transaction['credit'], each_transaction['date'], each_transaction['uuid'],
                                        each_transaction['store'])
    return 'added'

@app.route('/stores',methods=["GET"])
def stores_list():
    user = request.args.get('query')
    print(request.args)
    print(user)
    if user == 'spent':
        print("hit")
        stores = query_maker.get_stores_sum_spent()
    else:
        stores = query_maker.get_stores()
    return jsonify(stores)

@app.route('/transactions',methods=["GET"])
def get_transactions():
    stores = query_maker.get_transactions()
    list = []
    for each in stores:
        list.append(each[0])
    print(list)
    return jsonify(list)

@app.route('/createcategory',methods=["POST"]) #sitll need to add stuff
def create_category():
    category = request.args.get('category')
    if query_maker.category_exists(category):
        return "This category already exists"



#this function should return a list of stores and a list of cateogries to the client to sort
# @app.route('/categorizestores',methods=["PUT"])
# def init_categorize_stores():



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This will get logged')
    app.run(debug=True, threaded=True)
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 499
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
