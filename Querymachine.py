import mysql.connector
import config
from mysql.connector import errorcode


class Querymachine:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host=config.host,
                user=config.username,
                passwd=config.password,
                db='moneymanagedtest',
                port='3306',
                connect_timeout=5
            )
            self.cursor = self.mydb.cursor()
            self.drop_tables()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def drop_table(self, table_name):
        try:
            table_drop = 'DROP TABLE IF EXISTS ' + table_name + ';'
            self.cursor.execute(table_drop)
        except mysql.connector.Error as err:
            print("{} TABLE causing issues oof".format(table_name))
            print(err)
            raise mysql.connector.Error(err)

    def drop_tables(self):
        try:
            self.drop_table(config.store_table_name)
            self.drop_table(config.transaction_table)
        except mysql.connector.Error as err:
            print("Something went wrong while dropping:{}".format(err))

    def create_store_table(self):
        create_table = (
            "CREATE TABLE `{tablename}` ("
            "`{uuid}` VARCHAR (36) NOT NULL, "
            "`{name}` VARCHAR(200) NOT NULL, "
            "`{spent}` DECIMAL(13,4) DEFAULT '0.00', "
            "PRIMARY KEY (`{uuid}`))"
        ).format(tablename=config.store_table_name, uuid=config.store_uuid, name=config.store_name,
                 spent=config.store_spent)
        try:
            self.cursor.execute(create_table)
        except mysql.connector.Error as err:
            print("Error creating Store table as follows:{}".format(err))

    def create_transaction_table(self):
        create_table = (
            "CREATE TABLE `{tablename}`("
            "`{uuid}` VARCHAR (36) NOT NULL, "
            "`{amount}` DECIMAL (13,4) DEFAULT '0.00', "
            "`{date}` DATETIME, "
            "PRIMARY KEY (`{uuid}`));").format(tablename=config.transaction_table, uuid=config.store_uuid,
                                              date=config.transaction_date, amount=config.transaction_amount)
        try:
            self.cursor.execute(create_table)
        except mysql.connector.Error as err:
            print("Error creating tranascation table as follows:{}".format(err))

    def create_tables(self):
        self.create_store_table()
        self.create_transaction_table()

    def add_transaction(self, amount_spent, date, uuid):
        if amount_spent is '': #PLEASE FIX if amount_spent is not set (in the case where its a debit not a credit amount, refunds etc you need to set up some kind of option validation)
            amount_spent = 5
        insert_transaction = (
            "INSERT INTO `{table_name}` ("
            "`{field_uuid}`,`{amount}`,`{date}`)"
            " VALUES ('{t_id}',{value}, {t_date});"
        ).format(table_name=config.transaction_table, field_uuid=config.store_uuid,
                 date=config.transaction_date, amount=config.transaction_amount, t_id=uuid, t_date=date,
                 value=amount_spent)
        try:
            print(insert_transaction)
            self.cursor.execute(insert_transaction)
        except mysql.connector.Error as err:
            print("error inserting the {t_id} due t o {error}".format(t_id=uuid, error=err))

    def add_store(self, store_name, amt_spent):
        insert_store = (
            "INSERT INTO {table_name} ("
            "{uuid},{name},{spent})"
            " VALUES (UUID(),'{store}',{amt});"
        ).format(table_name=config.store_table_name, uuid=config.store_uuid, name=config.store_name,
                 spent=config.store_spent, store=store_name, amt=amt_spent)
        print(insert_store)
        try:
            self.cursor.execute(insert_store)
        except mysql.connector.Error as err:
            print("error inserting the {store} due to {error}".format(store=store_name, error=err))
