from pymongo import MongoClient
import pandas as pd

excel_file = 'Domande.xlsx'             
db_name = 'examly'             
collection_name = 'domande' 
mongo_url = "mongodb://admin:password@localhost:27017/"
client = MongoClient(mongo_url)
db = client[db_name]
collection = db[collection_name]
cursor = collection.find()  
df = pd.DataFrame(list(cursor))
df.drop(columns=["_id"], inplace=True)
