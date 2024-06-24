from hdfs import InsecureClient
from confluent_kafka import Producer
import json

def delivery_callback(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}'.format(msg.topic()))

def send_house_data(producer, topic, file_name, file_content):
    message = {
        "file_name": file_name,
        "content": file_content
    }
   
    producer.produce(topic, key=file_name, value=json.dumps(message), callback=delivery_callback)
    producer.poll(0)
    producer.flush()

hdfs_url = "http://localhost:9870"
data_lake_path = "/data_lake/house_prices"

client = InsecureClient(hdfs_url)
files_in_data_lake = client.list(data_lake_path)

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'python-producer'
}

producer = Producer(producer_conf)

for file_name in files_in_data_lake:
    hdfs_file_path = f"{data_lake_path}/{file_name}"
    with client.read(hdfs_file_path, encoding='utf-8') as reader:
        file_content = reader.read()
    
    for line in file_content.split("\n"):
        if line:
            send_house_data(producer, "house_data", file_name.split(".")[0], line)
    break
