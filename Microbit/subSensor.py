from microbit import *
import radio
id = "-"
chl = 1
data = ["DATA"]
data.append(str(chl))
data.append("")
data.append("")
data.append("")
radio.on()
radio.reset()
radio.config(queue=1)
while True:
    tmp = ""
    tmpArr = ""
    highest = ""
    if button_a.was_pressed():
        while True:
            #display.scroll("zz")
            radio.config(group=1)
            tmp = str(radio.receive())
            print(tmp)
            tmpArr = tmp.split(", ")
            if tmpArr[0] == "SENSORS" and id == "-":
                #Check for highest value
                highest = max(tmpArr[1:])
                print(highest)
                id = int(highest) + 1
                print(id)
                print(tmpArr)
                radio.config(group=0)
                radio.send("NEW, " + str(id))
                break
            sleep(100)
    if button_b.was_pressed():
        chl+= 1
        display.scroll("c-"+str(chl))
        radio.config(channel=chl)
        data[1] = str(chl)
        sleep(100)
    display.show(id)
    #collect data if id is set
    if id != "-":
        temp = str(temperature())
        data[3] = temp
        light = str(display.read_light_level())
        data[1] = str(chl)
        data[2] = str(id)
        data[4] = light
        radio.send(", ".join(data))
        sleep(6000)