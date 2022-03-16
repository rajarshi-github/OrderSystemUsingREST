import sqlite3
from sqlite3.dbapi2 import DatabaseError

from config import dbname
from dbcommon import tableExists
from dbcommon import dropTable

def createProductsTable():
    if tableExists('Products'):
        print("Table Products exists .. deleting ... ")
        dropTable('Products')

    try:
        connection = sqlite3.connect( dbname, check_same_thread=False)
        cursor = connection.cursor()

        createTableStmt = 'create table Products (' + \
                            'product_id integer primary key autoincrement,' + \
                            'name varchar(20),' + \
                            'price integer,' + \
                            'stock integer' + \
                            ');' 

        print(f"Executing statement : {createTableStmt}")
        cursor.execute(createTableStmt)
        cursor.close()
        connection.close()

    except DatabaseError as dbExcept:
        print("... Create Table \"Products\" failed. Error => ", dbExcept)

def createItemsTable():
    if tableExists('Items'):
        print("Table Items exists .. deleting ... ")
        dropTable('Items')

    try:
        connection = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connection.cursor()

        createTableStmt = \
                        'create table Items (' + \
                            'item_id integer primary key autoincrement, ' + \
                            'order_id integer references Orders(order_id), ' + \
                            'product_id varchar(20) references Products(product_id), ' + \
                            'quantity integer,' + \
                            'amount integer' + \
                        ');' 

        print(f"Executing statement : {createTableStmt}")

        cursor.execute(createTableStmt)

        cursor.close()
        connection.close()

    except DatabaseError as e:
        print("... Create Table \"Items\" failed. Error => ", e)

def createOrderTable():

    if tableExists('Orders'):
        print("Table Orders exists .. deleting ... ")
        dropTable('Orders')

    try:
        connection = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connection.cursor()

        createTableStmt = 'create table Orders (' + \
                            'order_id integer primary key autoincrement,' + \
                            'username varchar(20), ' + \
                            'order_date datetime default current_timestamp ' + \
                            ' );' 

        print(f"Executing statement : {createTableStmt}")

        cursor.execute(createTableStmt)

        cursor.close()
        connection.close()

    except DatabaseError as e:
        print("... Create Table \"Items\" failed. Error => ", e)


