import os
import pandas as pd

import products
import dbsetup

def readCSV(inputfile):
    try:
        if os.path.exists(inputfile):
            df = pd.read_csv(inputfile, header=None)
            df.columns = ['ProductName', 'Price', 'Stock']
            return df
        else:
            raise FileNotFoundError("File \"" + inputfile + "\" not found.")

    except FileNotFoundError as fileExcept:
        print(fileExcept)
    except:
        print("Other error")


def loadProductsFromCSV(inputFile):    
    print("Loading " + inputFile + " ... ")
    try:
        df = readCSV(inputfile=inputFile)
    except FileNotFoundError as e:
        print(e)
    else:
        for row in df.iterrows():
            products.addProductRecord(   \
                productName=row[1][0], \
                productPrice=row[1][1], \
                productStock=row[1][2] \
            )        

if __name__ == '__main__':
    try:
        dbsetup.createOrderTable()
        dbsetup.createProductsTable()
        dbsetup.createItemsTable()

        loadProductsFromCSV( os.getcwd() + '/products.csv')
    except Exception as e:
        print("Exited - Some Errors found => ", e)