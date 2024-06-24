import paho.mqtt.client as mqttClient
import time
import os
import pandas as pd

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

def on_publish(client, userdata, result):
    print("Data published \n")
    pass

Connected = False
broker_address = "broker.hivemq.com"
port = 1883

client = mqttClient.Client("house_data_sender")
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, port=port)
client.loop_start()

while not Connected: 
    time.sleep(0.1)

print("Connected to broker: ", broker_address, "\n")

try:
    while True:
        folder_path = 'house_data'
        csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

        for file in csv_files:
            df = pd.read_csv(folder_path + "/" + file)

            for row in df.to_numpy():
                message = {"house_id": file.split('.')[0]}
                for c, r in zip(df.columns, row):
                    message[c] = r
                topic = "house/data"
                client.publish(topic, payload=json.dumps(message))
                time.sleep(1)
                print("Message successfully published to house/data")

except KeyboardInterrupt:
    print("Exiting loop")
    client.disconnect()
    client.loop_stop()
