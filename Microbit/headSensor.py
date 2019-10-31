from microbit import *
import radio
chl = 1
# Turns on radio, resets it if preconfigurations are present
# Extends radio max message length to 251 bytes, change queue to 1
radio.on()
radio.reset()
radio.config(length=251)
radio.config(queue=1)
sensors = ["SENSORS", "1"]
display.show("1")
id = 1
head_data = [str(chl),"1"]
head_data.append("")
head_data.append("")
while True:
    tmp = ""
    tmpArr = ""
    # Change radio group to 1 and then send current sensor IDs out in a message
    radio.config(group=1)
    radio.send(", ".join(sensors))
    # Change back to group 0
    radio.config(group=0)
    tmp = str(radio.receive())
    # Convert the message into a array
    tmpArr = tmp.split(", ")
    # If ID that got recived over radio is not in sensor array, it will be placed there
    if tmpArr[0] == "NEW" and tmpArr[1:] not in sensors:
        sensors.append(tmpArr[1])
    # If the message is data, it will print out the recived data and also its own data
    if tmpArr[0] == "DATA":
        print(tmpArr[1:])
        temp = str(temperature())
        light = str(display.read_light_level())
        head_data[2] = temp
        head_data[3] = light
        print(head_data)
        head_data[2] = ""
        head_data[3] = ""
    # If 'B' button is pressed, change channel
    if button_b.was_pressed():
        chl+= 1
        display.scroll("c-"+str(chl))
        radio.config(channel=chl)
        head_data[0] = str(chl)
        #print("CHANGED")
        display.show("1")
        sleep(100)
    # If 'A' button is pressed, print 'EXIT' so raspberry pi can read over serial and run shutdown command
    if button_a.was_pressed():
        sleep(400)
        print("EXIT")
        break
    # If no other sensors are connected, print data
    if len(sensors) == 2:
        temp = str(temperature())
        light = str(display.read_light_level())
        head_data[2] = temp
        head_data[3] = light
        print(head_data)
        head_data[2] = ""
        head_data[3] = ""
        sleep(100)
        sleep(600)
