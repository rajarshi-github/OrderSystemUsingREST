import sqlite3
from sqlite3.dbapi2 import DatabaseError
from datetime import datetime
from random import randint

from config import addRecordFailed
from config import noSuchProduct
from config import success
from config import pageError
from config import notEnoughProductQuantity
from config import dbname
from config import dayLimit
from config import perPageLimitError
from config import perPage


import products
import items

def createNewOrderId():
    newOrderId = None
    createStatus = False
    try:
        connection = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connection.cursor()
        currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        userName = 'user' + str(randint(1000000,9999999))

        stmt = 'insert into Orders (username, order_date) values ( \'' + userName + '\' , \'' + currentTime + '\' );' 
        print(f"Executing statement : {stmt}")
        cursor.execute(stmt)

        connection.commit()
        newOrderId = cursor.lastrowid
        cursor.close()
        connection.close()

        createStatus = True
    except DatabaseError as e:
        print("... Create new order failed. Error => ", e)
    return (createStatus, newOrderId)

def addItemsToAnOrder(newOrderId, product, quantityRequested):
    productId = products.productExists(productName=product)
    if productId is not None:
        productDetails = products.getProductDetails(productId=productId)
        stock = int(productDetails[2])

        if stock > quantityRequested:
            
            price = productDetails[1]

            totalAmount = price * quantityRequested

            if newOrderId:
                products.reduceProductStock(productId, quantityRequested)
                items.addItems(orderId=newOrderId, productId=productId, quantity=quantityRequested, amount=totalAmount)
                return  {'status': success, 'order':newOrderId, 'product':productId, 'quantity':quantityRequested, 'amount':totalAmount}
            else:
                return addRecordFailed

                # 
                # delete record from Orders table 
                # if insert into Item has failed
                # 
                # not done yet
        else:
            return notEnoughProductQuantity
    else:
        return noSuchProduct

def addOrder(dictOfOrder):
    orderStatus = {}
    newOrderStatus, newOrderId = createNewOrderId()

    if newOrderStatus:
        slno = 0
        for item in dictOfOrder['items']: 
            status = addItemsToAnOrder(newOrderId=newOrderId, product=item['name'], quantityRequested=item['quantity'])
            orderStatus[slno] = { 'item': item['name'], 'quantity':item['quantity'],'status': status}
            slno += 1

    return orderStatus

def getOrderList():
    try:
        connection = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connection.cursor()

        stmt = 'select p.name, p.price, quantity, amount ' + \
                '   from items i, products p, orders o ' + \
                '   where   i.product_id = p.product_id and ' + \
                '           i.order_id = o.order_id and ' + \
                '           o.order_date > current_timestamp - ' + str(dayLimit)  + \
                '    order by o.order_date desc;' 

        print(f"Executing statement : {stmt}")
        resultSet = cursor.execute(stmt).fetchall()
        cursor.close()
        connection.close()

        return resultSet

    except DatabaseError as e:
        print("... Create new order failed. Error => ", e)

def getPaginatedResults(resultSet, url, page, limitPerPage):

    if limitPerPage <= 0:
        return perPageLimitError

    countRecord = len(resultSet)

    if page < 1:
        return pageError
    else:
        page = page - 1

    if countRecord < (page*limitPerPage) :
        return pageError

    obj = {}

    startingRecord = page * limitPerPage 
    #obj['StartingRecord'] = startingRecord
    obj['PerPageRecords'] = limitPerPage
    obj['TotalRecords'] = countRecord
    obj['PagesTotal'] = (countRecord // limitPerPage)+1

    if page >= (countRecord // limitPerPage):
        obj['PageNext'] = ''
        obj['RecordEndsAt'] = countRecord
    else:
        obj['PageNext'] = url + '?page=' + str(page + 2)
        obj['RecordEndsAt'] = startingRecord + limitPerPage - 1


    if page < 0:
        obj['PageNext'] = url + '?page=1' 
        obj['PagePrevious'] = ''
        obj['RecordStartsAt'] = -1
        obj['RecordEndsAt'] = -1
        obj['data'] = []
    elif page == 0:
        obj['PagePrevious'] = ''
        obj['RecordStartsAt'] = 0
        obj['data'] = resultSet[ startingRecord : startingRecord + limitPerPage  ]
    else:
        obj['PagePrevious'] =  url + '?page=' + str(page)
        obj['RecordStartsAt'] = startingRecord
        obj['data'] = resultSet[ startingRecord : startingRecord + limitPerPage ]

    return obj    



if __name__ == '__main__':
    dictOfOrder = { 
                 "items" : [{"name":"pythonbook-1", "quantity":1}, 
                            {"name":"javabook-1", "quantity":1},
                            {"name":"pythonbook-4", "quantity":2}
                        ]
                }
    orderStatus = addOrder(dictOfOrder)
    print(orderStatus)



    dictOfOrder = { 
                 "items" : [{"name":"pythonbook-1", "quantity":1000}, 
                            {"name":"javabook-1", "quantity":1},
                            {"name":"pythonbook-4", "quantity":2}
                        ]
                }
    orderStatus = addOrder(dictOfOrder)
    print(orderStatus)

    getOrderList()