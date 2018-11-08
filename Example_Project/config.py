
from pymongo import MongoClient

DATABASE = MongoClient()['photoDb']
DEBUG = True
client = MongoClient('localhost', 27017)
