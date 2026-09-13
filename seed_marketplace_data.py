"""
Agri Link — Marketplace & Buyer Data Seeder
Populates real farmer-listed crops, sample buyer orders, wishlist bookmarks, and reviews in SQLite.
"""

import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "agrilink.settings")
django.setup()

from apps.accounts.models import User
from apps.marketplace.models import Product, ProductImage, Order, Bookmark
from apps.core.models import Review
from apps.core.constants import OrderStatus, QuantityUnit, ReviewType

print("Seeding marketplace crop listings and buyer data...")

# 1. Ensure farmers exist
farmers = list(User.objects.filter(role="farmer"))
if not farmers:
    print("No farmers found! Creating default farmer.")
    farmer = User.objects.create_user(
        username="farmer_9842199881",
        phone="+919842199881",
        role="farmer",
        name="Ramesh Kumar (Farmer)",
        district="Coimbatore",
        state="Tamil Nadu",
        is_verified=True,
    )
    farmers = [farmer]

# Ensure buyer exists
buyer = User.objects.filter(role="buyer", phone__contains="9842199884").first()
if not buyer:
    buyer = User.objects.filter(role="buyer").first()
if not buyer:
    buyer = User.objects.create_user(
        username="buyer_9842199884",
        email="buyer@agrilink.in",
        phone="+919842199884",
        role="buyer",
        name="Aditi Sharma (Buyer)",
        district="Chennai",
        state="Tamil Nadu",
        is_verified=True,
    )
    buyer.set_password("Buyer@2026")
    buyer.save()
else:
    if not buyer.email:
        buyer.email = "buyer@agrilink.in"
    buyer.set_password("Buyer@2026")
    buyer.is_verified = True
    buyer.is_active = True
    buyer.save()

print(f"Assigning crops to {len(farmers)} farmers. Buyer: {buyer.name} ({buyer.phone})")

# Real crop listings data
crop_catalogs = [
    {
        "crop_name": "Organic Ponni Paddy (Rice)",
        "quantity": Decimal("2500.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("42.00"),
        "harvest_date": date.today() - timedelta(days=5),
        "location": "Coimbatore, Tamil Nadu",
        "description": "Premium quality naturally cultivated single-origin Ponni paddy. Harvested fresh with zero chemical pesticide residues. Moisture content certified < 13%. Ready for milling and immediate bulk dispatch.",
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Fresh Red Onions (Bellary Grade-A)",
        "quantity": Decimal("1800.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("28.00"),
        "harvest_date": date.today() - timedelta(days=3),
        "location": "Tiruppur, Tamil Nadu",
        "description": "Graded 45mm+ Bellary red onions. Well cured with dry outer skins ensuring 45+ days shelf stability. Suitable for supermarket retail distribution and wholesale food processing.",
        "image_url": "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Cavendish Banana (Export Grade)",
        "quantity": Decimal("1200.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("35.00"),
        "harvest_date": date.today() - timedelta(days=2),
        "location": "Erode, Tamil Nadu",
        "description": "Green unripe Cavendish bananas harvested at 80% maturity stage. Uniform calibration and blemish-free skin. Packed in ventilated corrugated boxes for long-haul refrigerated transport.",
        "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Fresh Hybrid Tomatoes (Field Picked)",
        "quantity": Decimal("1500.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("24.00"),
        "harvest_date": date.today() - timedelta(days=1),
        "location": "Salem, Tamil Nadu",
        "description": "Firm, deep red hybrid field tomatoes. High pulp density and solid pericarp ideal for puree manufacturing and retail supply chains. Grade-A sorted and pre-washed.",
        "image_url": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Fresh Sugarcane (Co-0238 Thick Cane)",
        "quantity": Decimal("8500.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("4.50"),
        "harvest_date": date.today() - timedelta(days=4),
        "location": "Namakkal, Tamil Nadu",
        "description": "Juicy Co-0238 sugarcane with 19-21% brix sugar recovery index. Cut fresh from field on confirmed purchase orders. Ideal for jaggery production and commercial juice bars.",
        "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Salem Finger Turmeric (High Curcumin)",
        "quantity": Decimal("750.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("115.00"),
        "harvest_date": date.today() - timedelta(days=12),
        "location": "Erode, Tamil Nadu",
        "description": "Sun-dried golden finger turmeric with certified 4.2% natural curcumin content. Polished and double boiled following traditional hygienic protocols. Laboratory test certificate available.",
        "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Pollachi Matured Coconuts (Large Nut)",
        "quantity": Decimal("3000.00"),
        "unit": QuantityUnit.PIECE,
        "price": Decimal("32.00"),
        "harvest_date": date.today() - timedelta(days=6),
        "location": "Pollachi, Tamil Nadu",
        "description": "Famous Pollachi sweet-water matured coconuts weighing 550g - 650g each. High copra yield and thick oil-rich kernel. De-husked and graded for immediate shipment.",
        "image_url": "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?q=80&w=800&auto=format&fit=crop",
    },
    {
        "crop_name": "Golden Sweet Corn (Sugar-75 Hybrid)",
        "quantity": Decimal("1100.00"),
        "unit": QuantityUnit.KG,
        "price": Decimal("26.00"),
        "harvest_date": date.today() - timedelta(days=2),
        "location": "Dindigul, Tamil Nadu",
        "description": "Sugar-75 hybrid sweet corn ears with tender kernels and exceptionally high sweetness. Chilled immediately post-harvest to preserve sugar conversion. Husk-on packaging.",
        "image_url": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?q=80&w=800&auto=format&fit=crop",
    },
]

created_products = []
for idx, crop_info in enumerate(crop_catalogs):
    farmer_user = farmers[idx % len(farmers)]
    
    prod, created = Product.objects.get_or_create(
        crop_name=crop_info["crop_name"],
        defaults={
            "farmer": farmer_user,
            "quantity": crop_info["quantity"],
            "unit": crop_info["unit"],
            "price": crop_info["price"],
            "harvest_date": crop_info["harvest_date"],
            "location": crop_info["location"],
            "description": crop_info["description"],
            "is_available": True,
        }
    )
    if created:
        ProductImage.objects.create(product=prod, image_url=crop_info["image_url"])
        print(f"Created crop: {prod.crop_name} (Rs.{prod.price}/{prod.unit}) by {farmer_user.name}")
    created_products.append(prod)

# 2. Seed Orders for Buyer if not existing
if Order.objects.filter(buyer=buyer).count() == 0 and len(created_products) >= 3:
    # Order 1: Active In-Transit Order
    p1 = created_products[0]
    o1 = Order.objects.create(
        product=p1,
        buyer=buyer,
        quantity=Decimal("300.00"),
        total_price=Decimal("300.00") * p1.price,
        status=OrderStatus.SHIPPED,
    )
    print(f"Created sample active order #{o1.id} for {buyer.name}: {p1.crop_name} (Status: SHIPPED)")

    # Order 2: Confirmed Order
    p2 = created_products[1]
    o2 = Order.objects.create(
        product=p2,
        buyer=buyer,
        quantity=Decimal("250.00"),
        total_price=Decimal("250.00") * p2.price,
        status=OrderStatus.CONFIRMED,
    )
    print(f"Created sample confirmed order #{o2.id} for {buyer.name}: {p2.crop_name} (Status: CONFIRMED)")

    # Order 3: Delivered Order (Past successful purchase)
    p3 = created_products[2]
    o3 = Order.objects.create(
        product=p3,
        buyer=buyer,
        quantity=Decimal("150.00"),
        total_price=Decimal("150.00") * p3.price,
        status=OrderStatus.DELIVERED,
    )
    print(f"Created sample delivered order #{o3.id} for {buyer.name}: {p3.crop_name} (Status: DELIVERED)")

# 3. Seed Wishlist Bookmarks for Buyer
if Bookmark.objects.filter(user=buyer).count() == 0 and len(created_products) >= 5:
    Bookmark.objects.get_or_create(user=buyer, product=created_products[3])
    Bookmark.objects.get_or_create(user=buyer, product=created_products[5])
    print("Created sample wishlist bookmarks for buyer.")

# 4. Seed Reviews for Buyer
if Review.objects.filter(reviewer=buyer).count() == 0 and len(farmers) > 0:
    Review.objects.create(
        reviewer=buyer,
        reviewee=created_products[2].farmer,
        target_id=str(created_products[2].id),
        review_type=ReviewType.FARMER,
        rating=5,
        comment="Outstanding banana produce! Delivered precisely at the scheduled time in temperature-controlled crates. Absolutely pristine quality and honest weight measurement. Will source weekly!",
    )
    print("Created sample verified review for farmer.")

print("Marketplace & Buyer seeding completed successfully!")
