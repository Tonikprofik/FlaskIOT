#!/usr/bin/python3

#-----------------------------------------------------------
# Script for loading mqtt messages from the things network
# Basic script
# Author: hans@eaaa.dk
# date: 16.11.18
# version: 1.0
# ----------------------------------------------------------
import psycopg2
from datetime import datetime

import paho.mqtt.client as mqtt
import json

APPID = "lora_one"
PSW = "ttn-account-v2.U-d1TutGJpEfli_LDOVEZdham2w8K9rp1L59V_Uctc8"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('+/devices/+/up')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global gpsx
    global gpsy
    msg_dict = json.loads(msg.payload)
    metadata = msg_dict.get('metadata')
    print(msg.topic+" "+str(msg.payload))
    gpsx = metadata.get('latitude')
    gpsy= metadata.get('longitude')
    print('The location of the node is {} latitude and {} longitude.'.format(metadata.get('latitude'),
                                                                             metadata.get('longitude')))
    insert_iotdata(gpsx, gpsy, 'goddag')



def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost", database="iotdata", user="postgres", password="tonikprofik")

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


def insert_iotdata(gpsx, gpsy, message):
    """ insert a new vendor into the vendors table """
    sql = """I"""

    query = "INSERT INTO  iotdata (gpsx, gpsy, messtype, messvalue, ts) VALUES (%s, %s, %s, %s, %s);"
    data = (gpsx, gpsy, message, -11, datetime.now())

    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(host="localhost", database="iotdata", user="postgres", password="tonikprofik")
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
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(APPID, password=PSW)
client.connect("eu.thethings.network", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()