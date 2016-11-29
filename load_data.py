import json
from pymongo import MongoClient

client = MongoClient()
db = client.yelp


def insert_data(collection_name):
    """Inserts yelp data from the specified file into the respective collection."""

    file_name = 'data/yelp_academic_dataset_%s.json' % collection_name
    collection = db[collection_name]

    with open(file_name, 'r') as data:
        x = 1
        container = []
        for line in data:
            print('Count: ' + str(x))
            x += 1

            json_line = json.loads(line)
            container.append(json_line)

            if len(container) >= 200:
                #         perform insert
                print("======================================")
                collection.insert_many(container)
                container.clear()

        if len(container) != 0:
            #     perform insert
            print("[===========================================]")
            collection.insert_many(container)
            container.clear()


insert_data("review")
