from microbit import *
import radio
chl = 1
radio.on()
radio.reset()
radio.config(queue=1)
sensors = ["SENSORS", "1",]
display.show("1")
id = 1
head_data = [str(chl),"1"]
head_data.append("")
head_data.append("")
while True:
    tmp = ""
    tmpArr = ""
    radio.config(group=1)
    radio.send(", ".join(sensors))
    radio.config(group=0)
    tmp = str(radio.receive())
    tmpArr = tmp.split(", ")
    if tmpArr[0] == "NEW" and tmpArr[1:] not in sensors:
        sensors.append(tmpArr[1])
    if tmpArr[0] == "DATA":
        print(tmpArr[1:])
        temp = str(temperature())
        light = str(display.read_light_level())
        head_data[2] = temp
        head_data[3] = light
        print(head_data)
        head_data[2] = ""
        head_data[3] = ""

    if button_b.was_pressed():
        chl+= 1
        display.scroll("c-"+str(chl))
        radio.config(channel=chl)
        head_data[0] = str(chl)
        #print("CHANGED")
        display.show("1")
        sleep(100)
    if len(sensors) == 2:
        temp = str(temperature())
        light = str(display.read_light_level())
        head_data[2] = temp
        head_data[3] = light
        print(head_data)
        head_data[2] = ""
        head_data[3] = ""
        sleep(600)
    sleep(100)