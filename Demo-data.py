#!/usr/bin/python
import psycopg2
from datetime import datetime


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="iotdata", user="postgres", password="farouq12")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insert_iotdata(message):
    """ insert a new vendor into the vendors table """
    sql = """I"""

    query = "INSERT INTO  iotdata (gpsx, gpsy, messtype, messvalue, ts) VALUES (%s, %s, %s, %s, %s);"
    data = (10.23, 10.24, message, -11, datetime.now())

    conn = None
    try:
        # connect to the PostgreSQL database
        conn = conn = psycopg2.connect(host="localhost", database="iotdata", user="postgres", password="farouq12")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query, data)

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    # connect()
    insert_iotdata('godnat')
