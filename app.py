from re import U
import flask 
from flask import Flask, json, request

import orders
from config import perPage
"""
Creates the server app.
"""

app = Flask(__name__)
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

@app.route('/home', methods=['GET'])
def home():
    '''
    Test CURL command: 
        curl --header  "Content-Type: application/json"  
                -request GET  
                "127.0.0.1:5000/home"
    
    Output dictionary:
        { "message" : "Welcome home !!! "}

    '''
    return {"message": "Welcome Home"}

@app.route('/orders', methods=['GET'])
def getOrders():
    '''
    Test CURL command :
    % curl -H  "Content-Type: application/json"  -X GET  "127.0.0.1:5000/orders?page=2"

    Output : 
    {
        "PerPageRecords":5,
        "PreviousPage":1,
        "StartingRecord":10,
        "TotalPages":14,
        "TotalRecords":68,
        "data":[
            ["javabook-1",30,1,30],
            ["pythonbook-4",25,2,50],
            ["javabook-1",30,1,30],
            ["pythonbook-4",25,2,50]],
        "next":"/orders?page=3"
    }

    '''
    pageNumber = int(request.args['page'] )
    allOrders = orders.getOrderList()
    
    return orders.getPaginatedResults(resultSet=allOrders, \
                                        url='127.0.0.1:5000/orders', \
                                        page=pageNumber, \
                                        limitPerPage=perPage
                                    )

@app.route('/createorder', methods=['POST'])
def createOrder():
    '''
    Test CURL command:

    curl  --header  "Content-Type: application/json"  
            --request POST 
            --data '{"items": [
                                {"name":"pythonbook-1", "quantity":100}, 
                                {"name":"javabook-1", "quantity":1}, 
                                {"name":"pythonbook-4", "quantity":2}
                            ]}' 
            127.0.0.1:5000/createorder
    
    Output dictionary: 

        {
            "0": {"item":"pythonbook-1","quantity":100,"status":{"message":"Not enough quantity"}},
            "1":{"item":"javabook-1","quantity":1,"status":{"amount":30,"order":12,"product":2,"quantity":1,"status":{"message":"Success"}}},
            "2":{"item":"pythonbook-4","quantity":2,"status":{"amount":50,"order":12,"product":13,"quantity":2,"status":{"message":"Success"}}}
        }

    '''
    dictOfOrders = request.get_json()
    orderDetails = orders.addOrder( dictOfOrder=dictOfOrders)
    return orderDetails



if __name__ == '__main__':
    app.run( debug = True)
