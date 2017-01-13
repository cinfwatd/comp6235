from pymongo import MongoClient
client = MongoClient()
db = client.yelp
#print(db.collection_names())


def get_latitude(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"latitude": 1}):
        return i['latitude']

def get_longitude(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"longitude": 1}):
        return i['longitude']

def get_review_count(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"review_count": 1}):
        return i['review_count']

def get_star_rating(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"stars": 1}):
        return i['stars']



print(get_latitude('m5hMJ7SPIK7are8SykvlvA'))