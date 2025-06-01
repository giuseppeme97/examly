from pymongo import MongoClient
import pandas as pd
from configs import Configuration
from io import BytesIO


class MongoConnector():
    def __init__(self):
        self.client = MongoClient(Configuration.get_server())
        self.db = Configuration.get_db()

    def get_all_collections(self) -> list:
        return self.client[self.db].list_collection_names()

    def new_collection(self, collection_name: str, content: bytes) -> None:
        df = pd.read_excel(BytesIO(content))
        data = df.to_dict(orient='records')
        collection = self.client[self.db][collection_name]
        collection.insert_many(data)

    def get_df_from_collection(self, collection: str) -> object:
        try:
            df = pd.DataFrame(list(self.client[self.db][collection].find()))
            df.drop(columns=["_id"], inplace=True)
            return df
        except:
            return None
