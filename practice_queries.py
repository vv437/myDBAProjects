from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
collection = db['products']

print("=== BASIC QUERIES ===\n")

count = collection.count_documents({})
print(f"1. Total products: {count}")

electronics = collection.find_one({'category' : 'Electronics'})
print(f"\n2. First Electronics product: {electronics['name']}")

expensive = list(collection.find({'price': {'$gt':500}}).limit(5))
print(f"\n3. Products > $500: {len(expensive)} found")
for p in expensive: 
    print(f"   - {p['name']}: ${p['price']}")

low_stock = list(collection.find({'stock': {'$lt': 10}}))    
print(f"\n4. Low Stock Products: {len(low_stock)}")

rated_high = list(collection.find({
    'rating' : {'$gte' : 4.0},
    'reviews' : {'$gte' : 100},
}).limit(3))
print(f"\n5. High rated (4+) with 100+ reviews: {len(rated_high)}")
