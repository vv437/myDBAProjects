from pymongo import MongoClient

# Connect to local MongoDB (Docker)
client = MongoClient('mongodb://localhost:27017/')

# Test connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB!")
    
    # Create database and collection
    db = client['ecommerce_db']
    collection = db['products']
    
    # Insert test document
    result = collection.insert_one({
        'name': 'Test Product',
        'price': 99.99,
        'category': 'Electronics'
    })
    
    print(f"Inserted document ID: {result.inserted_id}")
    
    # Retrieve it
    product = collection.find_one({'_id': result.inserted_id})
    print(f"Retrieved: {product}")
    
except Exception as e:
    print(f"Error: {e}")