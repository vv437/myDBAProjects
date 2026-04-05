from pymongo import MongoClient
from faker import Faker
import random

fake = Faker()

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
collection = db['products']

# Clear existing data
collection.delete_many({})

# Generate 100 fake products
products = []
for i in range(100):
    product = {
        'name': fake.catch_phrase(),
        'description': fake.text(max_nb_chars=200),
        'price': round(random.uniform(10, 1000), 2),
        'category': random.choice(['Electronics', 'Clothing', 'Home', 'Sports', 'Books']),
        'brand': fake.company(),
        'stock': random.randint(0, 100),
        'rating': round(random.uniform(1, 5), 1),
        'reviews': random.randint(0, 500),
        'tags': random.sample(['new', 'sale', 'bestseller', 'trending', 'limited'], k=random.randint(1, 3)),
        'created_at': fake.date_time_this_year()
    }
    products.append(product)

# Insert all products
result = collection.insert_many(products)
print(f"Inserted {len(result.inserted_ids)} products")

# Show sample
print("\nSample product:")
print(collection.find_one())