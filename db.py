import os
from dotenv import load_dotenv

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


load_dotenv()

class Db():
  client: MongoClient
  db: Database

  def __init__(self):
    self.client = MongoClient(os.getenv('MONGO_URI'))
    self.db = self.client['br']

  def collection(self, name: str) -> Collection:
    return self.db[name]

db = Db()
