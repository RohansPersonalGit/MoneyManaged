from flask import Flask
from Querymachine import Querymachine
app = Flask(__name__)
query_maker = Querymachine()
@app.route('/')
def main():
    return 'welcome to money managed'
@app.route('/reset')
def reset():
    query_maker.drop_tables()
    query_maker.create_store_table()
    return 'reset this shit'


if __name__ == '__main__':
    app.run()
