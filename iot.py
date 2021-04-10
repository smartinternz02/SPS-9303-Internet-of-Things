import time
import paho.mqtt.client as mqtt
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "1lhc4b"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "12345678"

# Initialize the device client.
L=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data["command"]=="ON":
                print("MOTOR ON")
                
                
        elif cmd.data["command"]=="OFF":
                print("MOTOR OFF")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #L=50
        #L=20
        L=100
        
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'level' : L }}
        #print data
        def myOnPublishCallback():
            print ("Published Level = %s " % L, "to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(5)
        deviceCli.commandCallback = myCommandCallback
        break

# Disconnect the device and application from the cloud
deviceCli.disconnect()
