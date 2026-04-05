from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
collection = db['products']

print("=== AGGREGATION PIPELINES ===\n")

# 1. Average price by category
print("1. Average price by category:")
pipeline = [
    {'$group': {
        '_id': '$category',
        'avg_price': {'$avg': '$price'},
        'count': {'$sum': 1}
    }},
    {'$sort': {'avg_price': -1}}
]
for doc in collection.aggregate(pipeline):
    print(f"   {doc['_id']}: ${doc['avg_price']:.2f} ({doc['count']} products)")

# 2. Top 5 highest rated products
print("\n2. Top 5 highest rated:")
pipeline = [
    {'$sort': {'rating': -1, 'reviews': -1}},
    {'$limit': 5},
    {'$project': {'name': 1, 'rating': 1, 'reviews': 1, 'price': 1, '_id': 0}}
]
for doc in collection.aggregate(pipeline):
    print(f"   {doc['name']}: {doc['rating']}★ ({doc['reviews']} reviews) - ${doc['price']}")

# 3. Stock status analysis
print("\n3. Stock status:")
pipeline = [
    {'$bucket': {
        'groupBy': '$stock',
        'boundaries': [0, 10, 50, 100],
        'default': 'Other',
        'output': {'count': {'$sum': 1}, 'avg_price': {'$avg': '$price'}}
    }}
]
for doc in collection.aggregate(pipeline):
    range_name = f"{doc['_id']}-{doc['_id']+10}" if doc['_id'] == 0 else \
                 f"{doc['_id']}-{doc['_id']+40}" if doc['_id'] == 10 else \
                 f"{doc['_id']}-{doc['_id']+50}" if doc['_id'] == 50 else 'Other'
    print(f"   Stock {range_name}: {doc['count']} products (avg ${doc['avg_price']:.2f})")

# 4. Tag analysis - unwind arrays
print("\n4. Most popular tags:")
pipeline = [
    {'$unwind': '$tags'},
    {'$group': {'_id': '$tags', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}},
    {'$limit': 5}
]
for doc in collection.aggregate(pipeline):
    print(f"   #{doc['_id']}: {doc['count']} products")