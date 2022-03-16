
from cgitb import reset
import sqlite3
from sqlite3.dbapi2 import DatabaseError


from config import dbname
import dbsetup
from dbcommon import tableExists

    
def productExists(productName):
    productID = None
    if tableExists('Products'):
        print("Table Products found ... ")
        try:
            connection = sqlite3.connect(dbname, check_same_thread=False)
            cursor = connection.cursor()
            
            stmt = 'select product_id from Products where name = \'' + productName + '\' ;' 

            print(f"Executing statement : {stmt}")

            cursor.execute(stmt)

            result = cursor.execute(stmt).fetchone()
            if result:
                productID = result[0]

            cursor.close()
            connection.close()
        except DatabaseError as e:
            print("... Insert failed. Error => ", e)

        return productID

def reduceProductStock(productId, quantity):
    status = False
    if tableExists('Products'):
        print("Table Products found ... ")
        try:
            connection = sqlite3.connect(dbname, check_same_thread=False)
            cursor = connection.cursor()
            stmt = 'update Products set stock = stock - ' + str(quantity) + ' where product_id = ' + str(productId) + ' ;' 
            print(f"Executing statement : {stmt}")
            cursor.execute(stmt)
            connection.commit()
            cursor.close()
            connection.close()
            status = True
        except DatabaseError as e:
            print("... Insert failed. Error => ", e)

    return status

def getProductDetails(productId):
    if tableExists('Products'):
        print("Table Products found ... ")

        try:
            connection = sqlite3.connect(dbname, check_same_thread=False)
            cursor = connection.cursor()
            
            stmt = 'select name, price, stock from Products where product_id = ' + str(productId) + ' ;' 

            print(f"Executing statement : {stmt}")

            productDetails = cursor.execute(stmt).fetchone()

            cursor.close()
            connection.close()
        except DatabaseError as e:
            print("... Insert failed. Error => ", e)

        return productDetails

def addProductRecord(productName, productPrice, productStock):        
    if tableExists('Products'):
        print("Table Products found ... ")
        try:
            connection = sqlite3.connect(dbname, check_same_thread=False)
            cursor = connection.cursor()
            existingProductId = productExists(productName=productName)
            if existingProductId is not None:
                stmt = 'update Products set price = ' + \
                                        str(productPrice) + \
                                        ' where product_id = ' + \
                                        str(existingProductId) + ';' 
            else:
                stmt = 'insert into Products (name, price, stock) values (' + \
                                        '\'' + productName + '\' ,' + \
                                        str(productPrice) + ',' + \
                                        str(productStock)  + \
                        ' );' 

            print(f"Executing statement : {stmt}")

            cursor.execute(stmt)
            connection.commit()
            cursor.close()
            connection.close()

        except DatabaseError as e:
            print("... Insert failed. Error => ", e)



if __name__ == '__main__':
    try:
        dbsetup.createOrderTable()
        dbsetup.createProductsTable()
        dbsetup.createItemsTable()
        addProductRecord(productName='ganja', productPrice=30, productStock=200)

    except Exception as e:
        print("Exited - Some Errors found => ", e)
