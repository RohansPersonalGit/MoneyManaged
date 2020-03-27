import mysql.connector
import config
from mysql.connector import errorcode

TABLES={}
TABLES['STORES'] = (
    "CREATE TABLE `{tablename}` ("
    "`{uuid}` VARCHAR (36) NOT NULL, "
    "`{name}` VARCHAR(200) NOT NULL, "
    "`{spent}` DECIMAL(13,4) DEFAULT '0.00', "
    "`{category}` VARCHAR (36), "
    "FOREIGN KEY (`{category}`) REFERENCES {category_table_name}(`{uuid}`), "
    "PRIMARY KEY (`{uuid}`))"
)
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
            self.cursor = self.mydb.cursor(buffered=True)
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
            print("{} TABLE causing issues while DROPING oof".format(table_name))
            print(err)
            raise mysql.connector.Error(err)

    def drop_tables(self):
        try:
            self.cursor.execute("SET foreign_key_checks = 0;")
            self.drop_table(config.store_table_name)
            self.drop_table(config.transaction_table)
            self.drop_table(config.category_table)
            self.cursor.execute("SET foreign_key_checks = 1;")
        except mysql.connector.Error as err:
            print("Something went wrong while dropping:{}".format(err))

    def create_category_table(self):
        create_category = (
            "CREATE TABLE `{tablename}` ("
            "`{uuid}` VARCHAR (36) NOT NULL, "
            "`{name}` VARCHAR(36) NOT NULL, "
            "`{spent}` DECIMAL(13, 4) DEFAULT '0.00', "
            "PRIMARY KEY (`{uuid}`))"
        ).format(tablename=config.category_table, uuid=config.table_uuid, name=config.name_field, spent=config.spent_field)
        try:
            self.cursor.execute(create_category)
            print("Category table created")
        except mysql.connector.Error as err:
            print("Error creating Category table as follows:{}".format(err))

    def create_store_table(self):
        create_table = (
            "CREATE TABLE `{tablename}` ("
            "`{uuid}` VARCHAR (36) NOT NULL, "
            "`{name}` VARCHAR(200) NOT NULL, "
            "`{category}` VARCHAR (36), "
            "FOREIGN KEY (`{category}`) REFERENCES {category_table_name}(`{uuid}`), "
            "PRIMARY KEY (`{uuid}`))"
        ).format(tablename=config.store_table_name, uuid=config.table_uuid, name=config.name_field,
                 spent=config.spent_field, category=config.store_category, category_table_name=config.category_table)
        try:
            print(create_table)
            self.cursor.execute(create_table)
        except mysql.connector.Error as err:
            print("Error creating Store table as follows:{}".format(err))

    def create_transaction_table(self):
        create_table = (
            "CREATE TABLE `{tablename}`("
            "`{uuid}` VARCHAR (36) NOT NULL, "
            "`{amount}` DECIMAL (13,4) DEFAULT '0.00', "
            "`{date}` DATETIME, "
            "`{store_id}` VARCHAR (36), "
            "FOREIGN KEY (`{store_id}`) REFERENCES {stores_table_name}(`{uuid}`), "
            "PRIMARY KEY (`{uuid}`));").format(tablename=config.transaction_table, uuid=config.table_uuid,
                                               date=config.transaction_date, amount=config.transaction_amount,
                                               store_id=config.transaction_table_foreign_key,
                                               stores_table_name=config.store_table_name)
        try:
            self.cursor.execute(create_table)
        except mysql.connector.Error as err:
            print("Error creating tranascation table as follows:{}".format(err))

    def create_tables(self):
        self.create_category_table()
        self.create_store_table()
        self.create_transaction_table()

    def get_stores(self):
        get_stores = (
            "SELECT `{column}` FROM `{table_name}`;"
        ).format(column=config.name_field, table_name=config.store_table_name)
        print(get_stores)
        try:
            for store in self.cursor.execute(get_stores, multi=True):
                if store.with_rows:
                    print("Rows produced by statement '{}':".format(get_stores))
                    return store.fetchall()
                else:
                    print("idk get stores fucked it only produced {}".format(store.rowcount))
        except mysql.connector.Error as err:
            print("error getting stores due to {}".format(err))

    def add_transaction(self, amount_spent, date, uuid, store):
        if amount_spent is '':  # PLEASE FIX if amount_spent is not set (in the case where its a debit not a credit
            # amount, refunds etc you need to set up some kind of option validation)
            amount_spent = 5
        store_uuid = self.get_store_id(store)
        if store_uuid is None:
            store_uuid = self.add_store(store)
        insert_transaction = (
            "INSERT INTO `{table_name}` ("
            "`{field_uuid}`,`{amount}`,`{date}`, `{store_id}`)"
            " VALUES ('{t_id}',{value}, {t_date}, '{store_uuid_value}');"
        ).format(table_name=config.transaction_table, field_uuid=config.table_uuid,
                 date=config.transaction_date, amount=config.transaction_amount, t_id=uuid, t_date=date,
                 value=amount_spent, store_id=config.transaction_table_foreign_key, store_uuid_value=store_uuid)
        try:
            print(insert_transaction)
            self.cursor.execute(insert_transaction)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print("error inserting the {t_id} due t o {error}".format(t_id=uuid, error=err))

    def add_store(self, store_name):
        store_uuid = self.cursor.execute("SELECT UUID();")
        store_uuid = self.cursor.fetchone()[0]
        insert_store = (
            "INSERT INTO {table_name} ("
            "{uuid},{name})"
            " VALUES ('{store_id}','{store}');"
        ).format(table_name=config.store_table_name, uuid=config.table_uuid, name=config.name_field,
                 spent=config.spent_field, store=store_name, store_id=store_uuid)
        print(insert_store)
        try:
            self.cursor.execute(insert_store)
            self.mydb.commit()
            print(self.cursor.lastrowid)
            return store_uuid
        except mysql.connector.Error as err:
            print("error inserting the {store} due to {error}".format(store=store_name, error=err))

    def category_exists(self, category):
        select_cat = "SELECT `{column}` FROM `{table_name}`;".format(column=config.store_category,
                                                                     table_name=config.store_table_name)
        try:
            for store in self.cursor.execute(select_cat):
                if store.rowcount > 0:
                    return True
                else:
                    return False
        except mysql.connector.Error as err:
            print("error checking category due to {}".format(err))

    def get_store_id(self, name):
        print(name)
        select_store = ("SELECT `{column}` FROM `{table_name}`"
                        "WHERE {store_name} = '{find_name}';"
                        ).format(column=config.table_uuid, table_name=config.store_table_name,
                                 store_name=config.name_field, find_name=name)
        try:
            result = self.cursor.execute(select_store)
            if result is not None:
                return result.fetchone()
            else:
                print("store not foudn")  # should cause a create store diaglue
                return None

        except mysql.connector.Error as err:
            print("error getting store_id due to {}".format(err))
