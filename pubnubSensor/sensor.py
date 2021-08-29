import sys
import Adafruit_DHT
import time, threading, json

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

myChannel = "SD3a"
sensorList = ["sensor"]
data = {}

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-6919a660-226c-11eb-90e0-26982d4915be'
pnconfig.publish_key = 'pub-c-213e5f7e-5e67-4544-8cac-70904aea009c'
pnconfig.uuid = '3b4ffd04-072e-11ec-9a03-0242ac130003'
pubnub = PubNub(pnconfig)


def humTemp():
    data["works"] = False
    print("Sensors started")
    while True:
        if data["works"]:
            humidity, temperature = Adafruit_DHT.read_retry(11,4)
      #  print('Temp:  {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))  
            publish(myChannel, {"tempHum": ": " + str(temperature) + "ºC | " + str(humidity) + "%"})
            #publish(myChannel, {"Humidity ": str(humidity)})
            time.sleep(1)




def publish(custom_channel, msg):
    pubnub.publish().channel(custom_channel).message(msg).pn_async(my_publish_callback)
    

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(myChannel).message('Device Connected').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
       try:
           print(message.message)
           msg = message.message
           key = list(msg.keys())
           if key[0] == "event":    #{"event": {"sensor_name" : True}}
               self.handleEvent(msg)
       except Exception as e:
           print("Received: ", message.message)
           print(e)
           pass


    def handleEvent(self, msg):
         global data
         eventData = msg["event"]
         key = list(eventData.keys())
         print(key)
         if key[0] in sensorList:
            if eventData[key[0]] is True:
                    data["works"] = True
            elif eventData[key[0]] is False:
                    data["works"] = False




if __name__ == "__main__":
    sensorsThread = threading.Thread(target = humTemp)
    sensorsThread.start() 
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(myChannel).execute()
