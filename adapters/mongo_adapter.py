import pymongo


class MongoDatabase:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.client = None
        self.db = None

    def connect(self, database_name):
        try:
            self.client = pymongo.MongoClient(self.host, self.port)
            self.db = self.client[database_name]
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        if self.client is not None:
            self.client.close()

    def execute_query(self, collection_name, query=None):
        collection = self.db[collection_name]
        if query is None:
            result = collection.find()
        else:
            result = collection.find(query)
        return list(result)

    def execute_query_async(self, collection_name, query, result_queue):
        collection = self.db[collection_name]
        if query is None:
            result = collection.find()
        else:
            result = collection.find(query)
        result_queue.put(list(result))

    def update_document(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = collection.update_one(query, update)
        if result.modified_count > 0:
            return collection.find_one(query)
        else:
            return None

