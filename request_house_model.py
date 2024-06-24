import requests
from cassandra.cluster import Cluster
import pandas as pd
import pymongo

class HouseCassandraHandler:
    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect()
        self.session.execute("USE HousePrices")

    def fetch_data(self):
        rows = self.session.execute("SELECT * FROM house_data")
        return pd.DataFrame(rows)

    def close(self):
        self.cluster.shutdown()

url = 'http://127.0.0.1:5000/api/house_price_model'

cassandra_handler = HouseCassandraHandler()
dataset = cassandra_handler.fetch_data()
cassandra_handler.close()

dataset.to_csv('house_data.csv', index=False)
response = requests.post(url, files={'data': open('house_data.csv', 'rb')})

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["mydatabase"]
mycol = mydb["house_prices"]

mycol.insert_one(response.json())
print("Model and predictions saved to MongoDB.")
