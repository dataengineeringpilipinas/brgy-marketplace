"""
Seed database with dummy data
"""
import asyncio
from datetime import datetime
from app.database import async_session, init_db
from app.models.user import User
from app.models.business import Business, BusinessItem, BusinessPhoto
from app.models.order import Order
from app.models.review import Review
from app.models.promo import Promo
from app.utils.auth import hash_password


async def seed_database():
    """Seed the database with dummy data."""
    await init_db()
    
    async with async_session() as db:
        # Create users
        users = []
        
        # Admin user
        admin = User(
            email="admin@barangay.com",
            password_hash=hash_password("admin123"),
            full_name="Barangay Admin",
            phone="09123456789",
            role="admin",
            address_zone="Zone 1",
            is_active=True
        )
        db.add(admin)
        await db.flush()
        users.append(admin)
        
        # Resident users
        residents_data = [
            {
                "email": "maria.santos@example.com",
                "password": "password123",
                "full_name": "Maria Santos",
                "phone": "09111111111",
                "address_zone": "Zone 1"
            },
            {
                "email": "juan.dela.cruz@example.com",
                "password": "password123",
                "full_name": "Juan dela Cruz",
                "phone": "09222222222",
                "address_zone": "Zone 2"
            },
            {
                "email": "ana.reyes@example.com",
                "password": "password123",
                "full_name": "Ana Reyes",
                "phone": "09333333333",
                "address_zone": "Zone 3"
            },
            {
                "email": "carlos.garcia@example.com",
                "password": "password123",
                "full_name": "Carlos Garcia",
                "phone": "09444444444",
                "address_zone": "Zone 1"
            }
        ]
        
        for user_data in residents_data:
            user = User(
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                full_name=user_data["full_name"],
                phone=user_data["phone"],
                role="resident",
                address_zone=user_data["address_zone"],
                is_active=True
            )
            db.add(user)
            await db.flush()
            users.append(user)
        
        # Create businesses
        businesses_data = [
            {
                "owner": users[1],  # Maria Santos
                "name": "Maria's Home Kitchen",
                "category": "Food",
                "operating_hours": "Mon-Sat 8AM-6PM",
                "location_zone": "Zone 1",
                "description": "Home-cooked Filipino meals and snacks. Specializing in adobo, sinigang, and fresh lumpia.",
                "is_verified": True,
                "verified_by": admin.id,
                "verified_at": datetime.utcnow(),
                "items": [
                    {"name": "Adobo", "description": "Classic Filipino adobo", "price": 120.00},
                    {"name": "Sinigang", "description": "Sour soup with vegetables", "price": 150.00},
                    {"name": "Lumpia", "description": "Fresh spring rolls", "price": 80.00},
                    {"name": "Lechon Kawali", "description": "Crispy fried pork", "price": 200.00}
                ]
            },
            {
                "owner": users[2],  # Juan dela Cruz
                "name": "Juan's Repair Shop",
                "category": "Repairs",
                "operating_hours": "Mon-Fri 9AM-5PM",
                "location_zone": "Zone 2",
                "description": "Expert repair services for appliances, electronics, and furniture.",
                "is_verified": True,
                "verified_by": admin.id,
                "verified_at": datetime.utcnow(),
                "items": [
                    {"name": "Appliance Repair", "description": "Refrigerator, washing machine, etc.", "price": 500.00},
                    {"name": "Electronics Repair", "description": "TV, computer, phone", "price": 300.00},
                    {"name": "Furniture Repair", "description": "Chairs, tables, cabinets", "price": 400.00}
                ]
            },
            {
                "owner": users[3],  # Ana Reyes
                "name": "Ana's Beauty Salon",
                "category": "Beauty",
                "operating_hours": "Tue-Sun 10AM-7PM",
                "location_zone": "Zone 3",
                "description": "Professional hair cutting, styling, and beauty services.",
                "is_verified": False,
                "items": [
                    {"name": "Haircut", "description": "Men's and women's haircut", "price": 150.00},
                    {"name": "Hair Color", "description": "Full hair coloring", "price": 800.00},
                    {"name": "Manicure", "description": "Nail care and polish", "price": 200.00},
                    {"name": "Pedicure", "description": "Foot care and polish", "price": 250.00}
                ]
            },
            {
                "owner": users[4],  # Carlos Garcia
                "name": "Carlos Tutoring Services",
                "category": "Services",
                "operating_hours": "Mon-Fri 3PM-8PM, Sat 9AM-12PM",
                "location_zone": "Zone 1",
                "description": "Private tutoring for elementary and high school students. Math, Science, English.",
                "is_verified": True,
                "verified_by": admin.id,
                "verified_at": datetime.utcnow(),
                "items": [
                    {"name": "Elementary Tutoring", "description": "1 hour session", "price": 300.00},
                    {"name": "High School Tutoring", "description": "1 hour session", "price": 400.00},
                    {"name": "Math Focus", "description": "Math-specific tutoring", "price": 350.00}
                ]
            },
            {
                "owner": users[1],  # Maria Santos (second business)
                "name": "Maria's Handmade Crafts",
                "category": "Crafts",
                "operating_hours": "By appointment",
                "location_zone": "Zone 1",
                "description": "Handmade bags, accessories, and home decor items.",
                "is_verified": False,
                "items": [
                    {"name": "Handmade Bag", "description": "Custom designed bag", "price": 500.00},
                    {"name": "Woven Accessories", "description": "Bracelets, keychains", "price": 150.00},
                    {"name": "Home Decor", "description": "Decorative items", "price": 300.00}
                ]
            },
            {
                "owner": users[2],  # Juan dela Cruz (second business)
                "name": "Juan's Equipment Rental",
                "category": "Rentals",
                "operating_hours": "Daily 8AM-6PM",
                "location_zone": "Zone 2",
                "description": "Rent tools, equipment, and party supplies.",
                "is_verified": True,
                "verified_by": admin.id,
                "verified_at": datetime.utcnow(),
                "items": [
                    {"name": "Power Tools", "description": "Drill, saw, etc. (per day)", "price": 500.00},
                    {"name": "Party Tent", "description": "Large tent rental (per day)", "price": 2000.00},
                    {"name": "Sound System", "description": "Speakers and microphone (per day)", "price": 1500.00}
                ]
            }
        ]
        
        businesses = []
        for biz_data in businesses_data:
            business = Business(
                owner_id=biz_data["owner"].id,
                name=biz_data["name"],
                category=biz_data["category"],
                operating_hours=biz_data["operating_hours"],
                location_zone=biz_data["location_zone"],
                description=biz_data["description"],
                is_verified=biz_data["is_verified"],
                verified_by=biz_data.get("verified_by"),
                verified_at=biz_data.get("verified_at"),
                is_active=True
            )
            db.add(business)
            await db.flush()
            businesses.append(business)
            
            # Add business items
            for item_data in biz_data["items"]:
                item = BusinessItem(
                    business_id=business.id,
                    name=item_data["name"],
                    description=item_data["description"],
                    price=item_data["price"],
                    is_available=True
                )
                db.add(item)
            
            # Add a primary photo placeholder
            photo = BusinessPhoto(
                business_id=business.id,
                image_url="https://via.placeholder.com/400x300?text=" + business.name.replace(" ", "+"),
                is_primary=True
            )
            db.add(photo)
        
        # Create some orders
        orders_data = [
            {
                "business": businesses[0],  # Maria's Home Kitchen
                "buyer": users[2],  # Juan dela Cruz
                "items": [{"item_id": 1, "quantity": 2, "price": 120.00}],
                "status": "completed",
                "notes": "Please deliver to Zone 2"
            },
            {
                "business": businesses[1],  # Juan's Repair Shop
                "buyer": users[3],  # Ana Reyes
                "items": [{"item_id": 5, "quantity": 1, "price": 300.00}],
                "status": "accepted",
                "notes": "TV repair needed"
            },
            {
                "business": businesses[2],  # Ana's Beauty Salon
                "buyer": users[4],  # Carlos Garcia
                "items": [{"item_id": 9, "quantity": 1, "price": 150.00}],
                "status": "pending"
            }
        ]
        
        orders = []
        for order_data in orders_data:
            order = Order(
                business_id=order_data["business"].id,
                buyer_id=order_data["buyer"].id,
                items=order_data["items"],
                status=order_data["status"],
                notes=order_data.get("notes")
            )
            db.add(order)
            await db.flush()
            orders.append(order)
        
        # Create a review for completed order
        if orders[0].status == "completed":
            review = Review(
                order_id=orders[0].id,
                business_id=orders[0].business_id,
                reviewer_id=orders[0].buyer_id,
                rating=5,
                comment="Excellent food! Very delicious and affordable. Will order again!",
                is_visible=True
            )
            db.add(review)
        
        # Create some promos
        promos_data = [
            {
                "business_id": businesses[0].id,
                "title": "Business of the Week",
                "description": "Maria's Home Kitchen - Best home-cooked meals in the barangay!",
                "promo_type": "business_of_week",
                "start_date": datetime.utcnow(),
                "created_by": admin.id
            },
            {
                "business_id": None,
                "title": "Newly Registered Businesses",
                "description": "Welcome our newest home-based businesses!",
                "promo_type": "newly_registered",
                "start_date": datetime.utcnow(),
                "created_by": admin.id
            },
            {
                "business_id": businesses[3].id,
                "title": "Verified Home Enterprise",
                "description": "Carlos Tutoring Services - Verified and trusted!",
                "promo_type": "verified",
                "start_date": datetime.utcnow(),
                "created_by": admin.id
            }
        ]
        
        for promo_data in promos_data:
            promo = Promo(**promo_data)
            db.add(promo)
        
        await db.commit()
        print("✅ Database seeded successfully!")
        print(f"   - Created {len(users)} users (1 admin, {len(users)-1} residents)")
        print(f"   - Created {len(businesses)} businesses")
        print(f"   - Created {len(orders)} orders")
        print(f"   - Created 1 review")
        print(f"   - Created {len(promos_data)} promos")


if __name__ == "__main__":
    asyncio.run(seed_database())

