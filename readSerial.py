#!/usr/bin/python3

import serial
import time
import pymysql
import json
import os
import threading
from serial.tools import list_ports
from datetime import datetime
from subprocess import call

# Scans serial ports after the micro bit
def serial_ports():

    '''
    Returns a generator for all available serial ports
    '''
    if os.name == 'nt':
        # windows
        _comports = [port for port in list_ports.comports()]
        if _comports.__len__() > 0:
            _serial_ports = [p for p in _comports[0]]
        else:
            _serial_ports = []
    else:
        # unix
        _serial_ports = [port[0] for port in list_ports.comports()]
    return _serial_ports
print(serial_ports())
# Opens the port, enabeling program to read from it
port = serial_ports()
baud = 115200
s = serial.Serial()
s.port = port[0]
s.open()
s.baudrate = baud
# Replace characters from incoming serial message
strReplace = "[]b\\r\\n'"
# Initiates collected data array
collectedData = []
# Tries to connect to remote database until sucessfull
while True:
    try:
        connection = pymysql.connect(host='remotemysql.com',
                                     db='krdhoQPq09',
                                     user='krdhoQPq09',
                                     passwd='sjMY2t9R4J')

        cursor = connection.cursor()
    except:
        print("connecting...")
        continue
    break
# Get current time from raspberry pi, then formatting it
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# Get upload rate from database table 'timer'
cursor.execute("""SELECT * from timer""")
upload = cursor.fetchone()
upload = str(upload)[1:-2]
connection.commit()

#Function that will run periodically in the background using 'threading'
def printit():

    threading.Timer(int(upload), printit).start()
    #If collected data array has values, push those to database
    if collectedData:
        for i in collectedData:

            mySql_insert_query = f"""INSERT INTO `sensors`(`Channel`, `ID`, `Tempature`, `Light`, `Uploaded`)
                                 VALUES
                                 ({i[0]}, {i[1]}, {i[2]}, {i[3]},
                                 '{dt_string}')"""
            result = cursor.execute(mySql_insert_query)
            print(mySql_insert_query)
            connection.commit()
printit()
while True:
    # update date
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    # Reads from serialport
    data = s.readline()
    data = data.decode("utf-8")
    # Replace unwanted characters
    for char in strReplace:
        data = data.replace(char, "")
        data = data.strip()
    # If micro bit sends 'EXIT', run command to shut down services and raspberry pi
    if data == "EXIT":
        call(['sudo', 'systemctl', 'poweroff'])
    data = data.split(", ")
    # If the array that stores the collected data is empty, add new data
    if len(collectedData) == 0:
        collectedData.append(data)
    found = False
    # Searches collected data array if sensordata is already in array, if found, replace.
    # If not found, add to array
    for c, array in enumerate(collectedData):
        if array[1] == data[1] and len(data) == 4:
                collectedData[c] = data
                found = True
    if not found and len(data) == 4:
        collectedData.append(data)
        found = False
    print(collectedData)

    time.sleep(1)
