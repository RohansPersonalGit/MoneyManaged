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
        print(create_table)
        self.cursor.execute(create_table)
