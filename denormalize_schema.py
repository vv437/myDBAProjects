from pymongo import MongoClient
from faker import Faker

fake = Faker()
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']

# Create separate collections for categories and brands
categories = db['categories']
brands = db['brands']

# Insert rich category documents
categories.insert_many([
    {
        '_id': 'Electronics',
        'description': 'Gadgets, devices, and electronic equipment',
        'tax_rate': 0.18,
        'return_policy': '30 days'
    },
    {
        '_id': 'Clothing',
        'description': 'Apparel and fashion items',
        'tax_rate': 0.12,
        'return_policy': '15 days'
    },
    {
        '_id': 'Home',
        'description': 'Furniture and home decor',
        'tax_rate': 0.12,
        'return_policy': '7 days'
    },
    {
        '_id': 'Sports',
        'description': 'Sports equipment and outdoor gear',
        'tax_rate': 0.18,
        'return_policy': '30 days'
    },
    {
        '_id': 'Books',
        'description': 'Physical and digital books',
        'tax_rate': 0.05,
        'return_policy': 'No returns'
    }
])

# Insert rich brand documents
brands.insert_many([
    {'_id': 'TechCorp', 'country': 'USA', 'website': 'techcorp.com', 'rating': 4.5},
    {'_id': 'FashionHub', 'country': 'Italy', 'website': 'fashionhub.it', 'rating': 4.2},
    {'_id': 'HomeStyle', 'country': 'Germany', 'website': 'homestyle.de', 'rating': 4.7},
    {'_id': 'SportMax', 'country': 'China', 'website': 'sportmax.cn', 'rating': 4.0},
    {'_id': 'BookWorld', 'country': 'UK', 'website': 'bookworld.co.uk', 'rating': 4.8}
])

print("Created categories and brands collections")

# Now create denormalized products with embedded rich data
products = db['products_denormalized']

# Sample: Embed category and brand details directly
sample_product = {
    'name': 'Smart Wireless Headphones',
    'price': 199.99,
    'category': {
        'name': 'Electronics',
        'tax_rate': 0.18,
        'return_policy': '30 days'
    },
    'brand': {
        'name': 'TechCorp',
        'country': 'USA',
        'rating': 4.5
    },
    'stock': 50,
    'tags': ['bestseller', 'wireless'],
    'reviews': [
        {'user': 'John', 'rating': 5, 'comment': 'Great sound!'},
        {'user': 'Jane', 'rating': 4, 'comment': 'Good but pricey'}
    ]
}

products.insert_one(sample_product)
print("Inserted denormalized product with embedded category, brand, and reviews")

# Query without joins - everything in one document
result = products.find_one()
print(f"\nSingle query gets all data:")
print(f"Product: {result['name']}")
print(f"Category tax: {result['category']['tax_rate']}")
print(f"Brand country: {result['brand']['country']}")
print(f"Reviews: {len(result['reviews'])}")