"""Sample product dataset for the shopping assistant"""

PRODUCTS = [
    {
        "id": "prod_001",
        "name": "Waterproof Rain Jacket",
        "description": "Lightweight waterproof jacket with sealed seams, perfect for rainy weather. Features adjustable hood and multiple pockets.",
        "category": "Outerwear",
        "price": 79.99,
        "tags": ["rainwear", "waterproof", "outdoor", "jacket", "women", "men"],
        "image_url": "/products/rain-jacket.jpg",
        "rating": 4.5,
        "in_stock": True,
        "brand": "WeatherPro"
    },
    {
        "id": "prod_002",
        "name": "Waterproof Hiking Boots",
        "description": "Durable waterproof hiking boots with excellent traction. Gore-Tex lining keeps feet dry in wet conditions.",
        "category": "Footwear",
        "price": 129.99,
        "tags": ["waterproof", "boots", "hiking", "outdoor", "shoes", "rainy weather"],
        "image_url": "/products/hiking-boots.jpg",
        "rating": 4.7,
        "in_stock": True,
        "brand": "TrailMaster"
    },
    {
        "id": "prod_003",
        "name": "Compact Travel Umbrella",
        "description": "Wind-resistant compact umbrella that fits in any bag. Auto open/close feature for convenience.",
        "category": "Accessories",
        "price": 24.99,
        "tags": ["umbrella", "rain", "compact", "travel", "accessories"],
        "image_url": "/products/umbrella.jpg",
        "rating": 4.3,
        "in_stock": True,
        "brand": "RainShield"
    },
    {
        "id": "prod_004",
        "name": "Waterproof Poncho",
        "description": "Lightweight emergency poncho that packs small. Perfect for unexpected rain during outdoor activities.",
        "category": "Outerwear",
        "price": 19.99,
        "tags": ["poncho", "rainwear", "waterproof", "emergency", "outdoor", "lightweight"],
        "image_url": "/products/poncho.jpg",
        "rating": 4.0,
        "in_stock": True,
        "brand": "QuickDry"
    },
    {
        "id": "prod_005",
        "name": "Black Cotton T-Shirt",
        "description": "Classic black cotton t-shirt with comfortable fit. Made from 100% organic cotton.",
        "category": "Apparel",
        "price": 29.99,
        "tags": ["shirt", "t-shirt", "black", "cotton", "casual", "basic"],
        "image_url": "/products/black-tshirt.jpg",
        "rating": 4.4,
        "in_stock": True,
        "brand": "EssentialWear"
    },
    {
        "id": "prod_006",
        "name": "Black Pullover Hoodie",
        "description": "Comfortable black hoodie with kangaroo pocket. Soft fleece lining for warmth.",
        "category": "Apparel",
        "price": 49.99,
        "tags": ["hoodie", "black", "casual", "sweatshirt", "warm"],
        "image_url": "/products/black-hoodie.jpg",
        "rating": 4.6,
        "in_stock": True,
        "brand": "UrbanStyle"
    },
    {
        "id": "prod_007",
        "name": "Classic Denim Jacket",
        "description": "Timeless denim jacket with button front. Perfect layering piece for any season.",
        "category": "Outerwear",
        "price": 69.99,
        "tags": ["denim", "jacket", "casual", "classic", "layering"],
        "image_url": "/products/denim-jacket.jpg",
        "rating": 4.8,
        "in_stock": True,
        "brand": "DenimCo"
    },
    {
        "id": "prod_008",
        "name": "White Cotton Tee",
        "description": "Essential white t-shirt made from premium cotton. Versatile wardrobe staple.",
        "category": "Apparel",
        "price": 27.99,
        "tags": ["shirt", "t-shirt", "white", "cotton", "essential", "basic"],
        "image_url": "/products/white-tee.jpg",
        "rating": 4.5,
        "in_stock": True,
        "brand": "EssentialWear"
    },
    {
        "id": "prod_009",
        "name": "Running Shoes - Breathable Mesh",
        "description": "Lightweight running shoes with breathable mesh upper. Cushioned sole for comfort during long runs.",
        "category": "Footwear",
        "price": 89.99,
        "tags": ["shoes", "running", "athletic", "breathable", "sports"],
        "image_url": "/products/running-shoes.jpg",
        "rating": 4.6,
        "in_stock": True,
        "brand": "RunFast"
    },
    {
        "id": "prod_010",
        "name": "Yoga Mat - Eco-Friendly",
        "description": "Non-slip yoga mat made from sustainable materials. Extra cushioning for joint support.",
        "category": "Fitness",
        "price": 39.99,
        "tags": ["yoga", "fitness", "eco-friendly", "exercise", "workout"],
        "image_url": "/products/yoga-mat.jpg",
        "rating": 4.7,
        "in_stock": True,
        "brand": "ZenFit"
    },
    {
        "id": "prod_011",
        "name": "Insulated Water Bottle",
        "description": "Stainless steel water bottle keeps drinks cold for 24 hours or hot for 12 hours. BPA-free.",
        "category": "Accessories",
        "price": 34.99,
        "tags": ["water bottle", "insulated", "stainless steel", "hydration", "eco-friendly"],
        "image_url": "/products/water-bottle.jpg",
        "rating": 4.8,
        "in_stock": True,
        "brand": "HydroFlow"
    },
    {
        "id": "prod_012",
        "name": "Wireless Earbuds - Noise Cancelling",
        "description": "Premium wireless earbuds with active noise cancellation. 30-hour battery life with charging case.",
        "category": "Electronics",
        "price": 149.99,
        "tags": ["earbuds", "wireless", "noise cancelling", "audio", "bluetooth"],
        "image_url": "/products/earbuds.jpg",
        "rating": 4.5,
        "in_stock": True,
        "brand": "SoundWave"
    },
    {
        "id": "prod_013",
        "name": "Laptop Backpack - Anti-Theft",
        "description": "Modern laptop backpack with USB charging port and anti-theft design. Fits up to 15.6 inch laptops.",
        "category": "Bags",
        "price": 59.99,
        "tags": ["backpack", "laptop", "travel", "anti-theft", "USB"],
        "image_url": "/products/backpack.jpg",
        "rating": 4.4,
        "in_stock": True,
        "brand": "TechCarry"
    },
    {
        "id": "prod_014",
        "name": "Sunglasses - UV Protection",
        "description": "Polarized sunglasses with 100% UV protection. Lightweight frame with stylish design.",
        "category": "Accessories",
        "price": 44.99,
        "tags": ["sunglasses", "UV protection", "polarized", "accessories", "eyewear"],
        "image_url": "/products/sunglasses.jpg",
        "rating": 4.3,
        "in_stock": True,
        "brand": "SunShield"
    },
    {
        "id": "prod_015",
        "name": "Smart Watch - Fitness Tracker",
        "description": "Feature-rich smartwatch with heart rate monitor, GPS, and sleep tracking. Water-resistant up to 50m.",
        "category": "Electronics",
        "price": 199.99,
        "tags": ["smartwatch", "fitness", "tracker", "GPS", "health"],
        "image_url": "/products/smartwatch.jpg",
        "rating": 4.6,
        "in_stock": True,
        "brand": "FitTech"
    }
]

DOCUMENTS = [
    {
        "id": "doc_001",
        "title": "How to Choose the Right Rain Gear",
        "content": """When selecting rain gear, consider these key factors:
        
1. Waterproof Rating: Look for products with at least 10,000mm waterproof rating for reliable protection.
2. Breathability: Choose materials that allow moisture to escape while keeping rain out.
3. Fit: Ensure comfortable fit that allows for layering underneath.
4. Features: Consider hoods, pockets, and adjustable elements.
5. Durability: Check seam sealing and quality of zippers.

Our waterproof rain jackets feature sealed seams and 15,000mm waterproof rating, while our hiking boots use Gore-Tex technology for ultimate protection.""",
        "doc_type": "guide",
        "category": "Outerwear",
        "tags": ["rainwear", "buying guide", "waterproof", "advice"]
    },
    {
        "id": "doc_002",
        "title": "FAQ: Product Returns and Exchanges",
        "content": """Q: What is your return policy?
A: We offer 30-day returns on all unused items in original packaging.

Q: How do I exchange a product?
A: Contact customer service with your order number and desired exchange item.

Q: Are there any items that cannot be returned?
A: Underwear, swimwear, and personalized items are final sale.

Q: How long do refunds take?
A: Refunds are processed within 5-7 business days of receiving the return.""",
        "doc_type": "FAQ",
        "category": "Customer Service",
        "tags": ["returns", "exchanges", "policy", "FAQ"]
    },
    {
        "id": "doc_003",
        "title": "Building the Perfect Capsule Wardrobe",
        "content": """A capsule wardrobe consists of essential, versatile pieces that work together:

Essential Items:
- Black and white t-shirts (basics that go with everything)
- Denim jacket (perfect layering piece)
- Black hoodie (casual comfort)
- Quality jeans (versatile bottom)
- Classic sneakers (everyday footwear)

Our black cotton t-shirts, black hoodies, and denim jackets are perfect foundations for any capsule wardrobe. Mix and match these pieces to create countless outfits.""",
        "doc_type": "guide",
        "category": "Fashion",
        "tags": ["wardrobe", "fashion", "styling", "basics"]
    },
    {
        "id": "doc_004",
        "title": "Caring for Your Waterproof Gear",
        "content": """Proper care extends the life of waterproof products:

1. Washing: Use gentle detergent, avoid fabric softener
2. Drying: Air dry or low heat tumble dry
3. Storage: Store in cool, dry place away from direct sunlight
4. Maintenance: Reapply DWR coating annually
5. Repairs: Fix small tears immediately to prevent spreading

Follow these steps to keep your rain jackets, boots, and ponchos performing at their best.""",
        "doc_type": "tutorial",
        "category": "Care Instructions",
        "tags": ["maintenance", "waterproof", "care", "tutorial"]
    },
    {
        "id": "doc_005",
        "title": "Fitness Gear Essentials for Beginners",
        "content": """Starting your fitness journey? Here's what you need:

1. Proper Footwear: Invest in quality running shoes with good cushioning
2. Yoga Mat: Essential for stretching and floor exercises
3. Water Bottle: Stay hydrated with an insulated bottle
4. Fitness Tracker: Monitor your progress with a smartwatch
5. Comfortable Clothing: Breathable, moisture-wicking fabrics

Our running shoes, yoga mats, and insulated water bottles are perfect for beginners. The smartwatch helps track your progress and stay motivated.""",
        "doc_type": "guide",
        "category": "Fitness",
        "tags": ["fitness", "beginners", "workout", "gear"]
    },
    {
        "id": "doc_006",
        "title": "Tech Accessories Buying Guide",
        "content": """Choose the right tech accessories for your lifestyle:

Wireless Earbuds: Look for battery life, noise cancellation, and comfort
Laptop Backpacks: Consider size, organization, and security features
Smartwatches: Check compatibility, battery life, and features

Our wireless earbuds offer 30-hour battery life and active noise cancellation. The anti-theft laptop backpack includes USB charging ports for convenience.""",
        "doc_type": "guide",
        "category": "Electronics",
        "tags": ["tech", "accessories", "buying guide", "electronics"]
    }
]
