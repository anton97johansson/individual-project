import serial, time
import mysql.connector
from mysql.connector import Error
import json
import os
import threading
from serial.tools import list_ports
from datetime import datetime
def serial_ports():
    '''
    Returns a generator for all available serial ports
    '''
    if os.name == 'nt':
        # windows
        _comports = [port for port in list_ports.comports()]
        if _comports.__len__()>0:
            _serial_ports = [p for p in _comports[0]]
        else:
            _serial_ports = []
    else:
        # unix
        _serial_ports = [port[0] for port in list_ports.comports()]
    return _serial_ports
print(serial_ports())
port = serial_ports()
baud = 115200
s = serial.Serial()
s.port = port[0]
s.open()
s.baudrate = baud
strReplace = "[]b\\r\\n'"
collectedData = []
#Tries to connect to remote database
try:
    connection = mysql.connector.connect(host='remotemysql.com',
                                         database='krdhoQPq09',
                                         user='krdhoQPq09',
                                         password='sjMY2t9R4J',
                                         port='3306')

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
def printit():
  threading.Timer(10, printit).start()
  if collectedData:
      for i in collectedData:

         mySql_insert_query = f"""INSERT INTO `sensors`(`Channel`, `ID`, `Tempature`, `Light`, `Uploaded`)
                                 VALUES
                                 ({i[0]}, {i[1]}, {i[2]}, {i[3]}, '{dt_string}')"""
         result = cursor.execute(mySql_insert_query)
         print(mySql_insert_query)
         connection.commit()
printit()
while True:
    now = datetime.now()

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    data = s.readline()
    data = data.decode("utf-8")
    for char in strReplace:
        data = data.replace(char, "")
        data = data.strip()

    data = data.split(", ")
    # print(data)
    # print(len(collectedData))
    if len(collectedData) == 0:
        collectedData.append(data)
    found = False
    for c, array in enumerate(collectedData):
            # collectedData.append(data)
        if array[1] == data[1]:
                collectedData[c] = data
                found = True
    # for array in collectedData:
    #         # collectedData.append(data)
    #     if array[1] == data[1]:
    #             found = True
    if not found:
        collectedData.append(data)
        found = False
    print(collectedData)

    time.sleep(1)
