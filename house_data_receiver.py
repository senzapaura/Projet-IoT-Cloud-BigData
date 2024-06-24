import paho.mqtt.client as mqtt
import time
import json
from hdfs import InsecureClient

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                
        Connected = True               
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    data_values = ",".join([str(value) for key, value in data.items() if key != "house_id"])
    local_file = data["house_id"]+'.csv'
    
    with open("csv_data/"+local_file, 'a') as file:
        file.write(data_values + "\n")

    hdfs_file_path = f"{data_lake_path}/{local_file}"
    if not hdfs_client.status(hdfs_file_path, strict=False):
        hdfs_client.upload(hdfs_file_path, "csv_data/"+local_file)
    
    print("Data saved to HDFS")

Connected = False
 
broker_address = "broker.hivemq.com"
port = 1883                   
 
hdfs_url = "http://localhost:9870"
hdfs_client = InsecureClient(hdfs_url)
data_lake_path = "/data_lake/house_prices"
if not hdfs_client.status(data_lake_path, strict=False):
    hdfs_client.makedirs(data_lake_path)
 
client = mqtt.Client("house_data_receiver")
client.on_message = on_message
client.on_connect = on_connect
client.connect(broker_address, port)  
client.loop_start()                   

while not Connected:                  
    time.sleep(0.1)
 
client.subscribe("house/data")
 
try:
    while True: 
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")
    client.disconnect()
    client.loop_stop()
