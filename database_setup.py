import json
import sys
import psycopg2

connection = psycopg2.connect(host='localhost', database='postgres', user='postgres', password='horses12')
cursor = connection.cursor()

def create_table(connection):
    sql = """CREATE TABLE bitcoin_data
    (bitcoin_date varchar(100),
    closing_price varchar(100))"""
    cursor.execute(sql)
    cursor.close()
    connection.commit()

create_table(connection)