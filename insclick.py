import argparse
import json
import sys
import os
import time
from shutil import copyfile

def loadclick():
    parser = argparse.ArgumentParser(description = "CLI for inserting/removing Mikroe Clicks through Greybus")
    parser.add_argument('-c', '--click', type=str, help='Click name : rtc6 , weather ', required=True)
    parser.add_argument('-p', '--port', type=str, help='Port number : p1 , p2 ..', required=True)
    args = parser.parse_args()
    platform=getPlatform()
    if(platform=="PB"):
        if(args.port.lower()=="p1"):
            port="PBP1"
        elif(args.port.lower()=="p2"):
            port="PBP2"
        else:
            print("PocketBeagle Supports only p1 and p2 slots")
            sys.exit(1)
    elif(platform=="BB"):
        if(args.port.lower()=="p1"):
            port="BBP1"
        elif(args.port.lower()=="p2"):
            port="BBP2"
        elif(args.port.lower()=="p3"):
            port="BBP3"
        elif(args.port.lower()=="p4"):
            port="BBP4"
        else:
           print("Beaglebone Black Supports only p1,p2,p3 and p4 slots")
           sys.exit(1) 
    with open('clicks.json') as f:
        clickdatajson = json.load(f)
    clickdata=clickdatajson[args.click]
    with open('pinconfig.json') as f:
        pindatajson = json.load(f)
    pindata=pindatajson[port]
    if(clickdata["type"]=="i2c"):
        for pins in pindata["i2cpins"]:
            os.system("config-pin "+ pins +" "+pindata["i2cpins"][pins])
        if(pindata["I2C"]=="i2c1"):
            copyfile("manifests/i2c1.mnfb", "/tmp/gbsim/hotplug-module/i2c1.mnfb")
        elif(pindata["I2C"]=="i2c2"):
            copyfile("manifests/i2c2.mnfb", "/tmp/gbsim/hotplug-module/i2c1.mnfb")
        time.sleep(3)
        os.system("echo "+ clickdata["driver"] +" "+ clickdata["address"] + " | sudo tee /sys/class/i2c-adapter/i2c-3/new_device") # 3 needs to be changed    
    else:
        print("Only I2C Clicks Supported")
        sys.exit(1)
    
def getPlatform():
    with open('/proc/device-tree/model','r') as f:
       model=f.readline()
       if(model.find("PocketBeagle")!=-1):
        return "PB"
       else :
        return "BB"



if __name__ == '__main__':
    loadclick()