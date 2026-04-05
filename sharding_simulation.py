from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
products = db['products']

print("=== SHARDING SIMULATION ===\n")

# Simulate shard distribution by category
# In real MongoDB: sh.enableSharding("ecommerce_db")
#                sh.shardCollection("ecommerce_db.products", {"category": 1})

categories = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books']

print("1. Simulated Shard Distribution (by category):")
for cat in categories:
    count = products.count_documents({'category': cat})
    avg_price = list(products.aggregate([
        {'$match': {'category': cat}},
        {'$group': {'_id': None, 'avg': {'$avg': '$price'}}}
    ]))
    avg = avg_price[0]['avg'] if avg_price else 0
    print(f"   Shard '{cat}': {count} documents, avg price ${avg:.2f}")

print("\n2. Range-based Sharding Simulation (by price):")
ranges = [
    ('Budget', 0, 100),
    ('Mid-range', 100, 500),
    ('Premium', 500, 1000)
]
for name, min_p, max_p in ranges:
    count = products.count_documents({'price': {'$gte': min_p, '$lt': max_p}})
    print(f"   Shard '{name}' (${min_p}-${max_p}): {count} documents")

print("\n3. Query Routing (simulated):")
# Good shard key: query targets specific shard
cat_query = products.find({'category': 'Electronics'}).limit(3)
print(f"   Query 'category=Electronics' → routed to Electronics shard")
print(f"   Found: {len(list(cat_query))} products")

# Bad shard key: scatter-gather query
price_query = products.find({'price': {'$gt': 800}}).limit(3)
print(f"   Query 'price>800' → must check ALL shards (scatter-gather)")
print(f"   Found: {len(list(price_query))} products")

print("\n4. Shard Key Recommendation:")
print("   For e-commerce: {'category': 1, 'created_at': 1}")
print("   - Even distribution by category")
print("   - Time-based queries efficient")
print("   - Avoid monotonic _id (creates hot shards)")