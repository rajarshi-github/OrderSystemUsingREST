import sqlite3
from sqlite3.dbapi2 import DatabaseError

from config import addRecordFailed
from config import noSuchProduct
from config import success
from config import noSuchProduct
from config import dbname


def addItems(orderId, productId, quantity, amount):
    itemAdded = False
    try:
        connection = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connection.cursor()
        stmt = 'insert into Items (order_id, product_id, quantity, amount) values ( ' + \
                    str(orderId) + ',' + \
                    str(productId) + ',' + \
                    str(quantity) + ',' + \
                    str(amount) +  \
                 ');' 
        print(f"Executing statement : {stmt}")
        cursor.execute(stmt)
        connection.commit()
        cursor.close()
        connection.close()
        itemAdded = True
    except DatabaseError as e:
        print("... Create new order failed. Error => ", e)
    return itemAdded

    