from microbit import *
import radio
id = "-"
chl = 1
data = ["DATA"]
data.append(str(chl))
data.append("")
data.append("")
data.append("")
# Turn on radio
radio.on()
# reset radio if configured
radio.reset()
# config queue to 1 and max length to 251
radio.config(queue=1)
radio.config(length=251)
while True:
    tmp = ""
    tmpArr = ""
    highest = ""
    # if button 'A' is pressed, it will change radio group to 1, where current IDs in the system is
    # broadcasted
    if button_a.was_pressed():
        while True:
            #display.scroll("zz")
            radio.config(group=1)
            tmp = str(radio.receive())
            print(tmp)
            tmpArr = tmp.split(", ")
            if tmpArr[0] == "SENSORS" and id == "-":
                # Check for highest value
                print(tmpArr)
                tmpArr = list(map(float, tmpArr[1:]))
                highest = max(tmpArr)
                # Gives id a value over the highest value in the array
                id = float(highest) + 1
                id = str(id)

                #print(id.split(".")[0])
                id = id.split(".")[0]
                # reconfigures to group 0, where data is being transmitted
                radio.config(group=0)
                # Sends radio message with the id it got, so head sensor can pick it up and add to array of IDs
                radio.send("NEW, " + str(id))
                print("NEW, " + str(id))
                break
            elif id != "-":
                break
            sleep(100)
    # If 'B' button is pressed, change radio channel
    if button_b.was_pressed():
        chl+= 1
        display.scroll("c-"+str(chl))
        radio.config(channel=chl)
        data[1] = str(chl)
        sleep(100)
    display.scroll(str(id), wait=False, loop=True)
    #collect data if id is set and send over radio as a string
    if id != "-":
        temp = str(temperature())
        data[3] = temp
        light = str(display.read_light_level())
        data[1] = str(chl)
        data[2] = str(id)
        data[4] = light
        radio.send(", ".join(data))
        sleep(6000)
