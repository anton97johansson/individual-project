README for microbit project
==

Intro
---
Microbits will send data to a microbit that is connected via USB to a raspberry pi.
The microbit that is connected to a raspberry pi will send data over serial port.
Raspberry pi has a script that will run on start up, that script will read serial port
and upload to database.

The database is running on remotemysql.com

[phpMyAdmin for database](https://remotemysql.com/phpmyadmin/)

Languages:
* Python 3 (raspberry pi)
* Micropython (microbits)

Dependencies:
* Pyserial
* PyMySQL


Setup
--

Microbit:

* [Install MU](https://codewith.mu/en/download)
* Flash one microbit with 'headSensor.py', this will be the head sensor
* Flash all other microbits with 'subSensor.py'

Raspberry pi:

* Get readSerial.py on to the raspberry pi, change permissions on file
        chmod u+x readSerial.py
* Install dependencies on raspberry pi

        pip3 install pyserial
        pip3 install PyMySQL

* Create a service
        pi ~$ sudo systemctl edit --force --full readSerial.service
Inside the file, paste this

**Note the path to where you placed the script AKA working directory**

        [Unit]
        Description=My Script Service
        Wants=network-online.target
        After=network-online.target

        [Service]
        Type=simple
        User=pi
        WorkingDirectory=/home/pi/script
        ExecStart=/home/pi/script/readSerial.py

        [Install]
        WantedBy=multi-user.target
Exit editor and write
        pi ~$ sudo systemctl enable readSerial.service
        pi ~$ sudo systemctl start readSerial.service
        pi ~$ sudo systemctl reboot

How to use
----
Connect the raspberry pi to a network. (Easiest done with the user interface)

If wifi has been setup you can do two things:

Start script manually

or write in terminal

    sudo systemctl restart readSerial.service
The above command will restart services. So plug in the head sensor before.
_____

If wifi is already set up on raspberry pi, then all you need to do is start the raspberry pi with head microbit connected.
Then you can connect additional microbits (given that they are flashed with the sub sensor script) by pressing the 'A' button to get a unique ID or if you need to change channel first, press 'B'.

The raspberry pi uploads every 5 min, if you want to change the upload rate, then you can change the number in the timer table at the database. It's in seconds (300s = 5 min)
