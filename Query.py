__author__ = 'GIS336'
import pandas as pd
import sqlite3
def query_all(dbConn):
    return pd.read_sql("select * from store;", dbConn)
