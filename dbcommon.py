from re import I
import sqlite3
from sqlite3.dbapi2 import DatabaseError

from config import dbname


def tableExists(tableName):
    tablenames = []
    try:
        connect = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connect.cursor()
        stmt = "select tbl_name from sqlite_master where type = \'table\' and tbl_name = \'" + \
                tableName + "\' order by tbl_name; "
        tablenames = cursor.execute(stmt).fetchall()
        cursor.close()
        connect.close()
    except DatabaseError as dbExcept:
        print('... Database Error => ', dbExcept)
    
    if tablenames[0][0] == tableName and len(tablenames) == 1:
        return True
    else:
        return False

def dropTable(tableName):
    try:
        connect = sqlite3.connect(dbname, check_same_thread=False)
        cursor = connect.cursor()
        stmt = "drop table " + tableName + " ; "
        cursor.execute(stmt)
        cursor.close()
        connect.close()
        print ("Table " + tableName + " dropped.")
    except DatabaseError as dbExcept:
        print("... Drop table failed" , dbExcept)
