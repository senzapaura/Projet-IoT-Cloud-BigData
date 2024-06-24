from confluent_kafka import Consumer, KafkaError
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, FloatType
from pyspark.sql.functions import col, mean
import numpy as np
from cassandra.cluster import Cluster

class HouseCassandraHandler:
    def __init__(self, create_keyspace_command, data):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute(create_keyspace_command)
        self.session.execute("USE HousePrices")
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS house_data (
                area FLOAT,
                bedrooms FLOAT,
                bathrooms FLOAT,
                stories FLOAT,
                parking FLOAT,
                price FLOAT
            )
        """)
        self.session.execute("TRUNCATE house_data")
        self.insert_data(data)

    def insert_data(self, data):
        for d in data:
            self.session.execute(f"""
                INSERT INTO house_data (area, bedrooms, bathrooms, stories, parking, price)
                VALUES ({d[0]}, {d[1]}, {d[2]}, {d[3]}, {d[4]}, {d[5]})
            """)

    def close(self):
        self.cluster.shutdown()

def fetch_house_data(consumer, topic):
    consumer.subscribe([topic])
    house_data = []
    print("Waiting for messages...")
    first_message = False

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            if first_message:
                break
            else:
                continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        try:
            first_message = True
            data = json.loads(msg.value())
            row = data["content"].split(",")
            if len(row) == 6:
                row = [float(x) for x in row]
                house_data.append(row)
            
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
        except KeyError as e:
            print(f"Missing Key in JSON: {e}")

    consumer.close()
    print("Completed")
    return house_data

def preprocess_house_data(house_data):
    spark = SparkSession.builder.appName('HouseData').getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType([
        StructField("area", FloatType(), True),
        StructField("bedrooms", FloatType(), True),
        StructField("bathrooms", FloatType(), True),
        StructField("stories", FloatType(), True),
        StructField("parking", FloatType(), True),
        StructField("price", FloatType(), True)
    ])

    df = spark.createDataFrame(house_data, schema)
    df = df.groupBy().agg(
        mean("area").alias("area"),
        mean("bedrooms").alias("bedrooms"),
        mean("bathrooms").alias("bathrooms"),
        mean("stories").alias("stories"),
        mean("parking").alias("parking"),
        mean("price").alias("price")
    )

    return df.collect()

# Kafka consumer configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
house_data = fetch_house_data(consumer, "house_data")
preprocessed_data = preprocess_house_data(house_data)

# Cassandra keyspace configuration
keyspace_name = 'HousePrices'
replication_strategy = 'SimpleStrategy'
replication_factor = 3

create_keyspace_query = f"""
    CREATE KEYSPACE IF NOT EXISTS {keyspace_name}
    WITH replication = {{'class': '{replication_strategy}', 'replication_factor': {replication_factor}}};
"""

cassandra_handler = HouseCassandraHandler(create_keyspace_query, preprocessed_data)
cassandra_handler.close()