#!/bin/sh
# This script will subscribe to
# things network lora_one node

HOST="eu.thethings.network"
TOPIC="+/devices/+/up"
APP_ID="lora_one"
ACCESS_KEY="ttn-account-v2.U-d1TutGJpEfli_LDOVEZdham2w8K9rp1L59V_Uctc8"

mosquitto_sub -h $HOST -t $TOPIC -u $APP_ID -P $ACCESS_KEY -v