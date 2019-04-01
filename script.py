import time
from sds011 import SDS011
import configparser
import pymongo
import datetime

config = configparser.ConfigParser()
config.read("config.txt")

client = pymongo.MongoClient(config["mongodb"]["connection"])
db = client[config["mongodb"]["database"]]
collection = db[config["mongodb"]["collection"]]

sensor = SDS011(config["sensor"]["port"], use_query_mode=True)

while True:
    v = sensor.query()
    entry = {
        "time": datetime.datetime.now(),
        "location": config["sensor"]["location"],
        "pm25": v[0],
        "pm10": v[1]
    }
    id = collection.insert_one(entry).inserted_id
    print("%(time)s %(location)s %(pm25)s %(pm10)s" % entry)
    time.sleep(int(config["sensor"]["sleep"]))
