"""
Agri Link — Constants & Enumerations
======================================
Centralized constants used across the entire project.
"""


# ---- User Roles ----
class UserRole:
    FARMER = "farmer"
    BUYER = "buyer"
    LABOUR = "labour"
    EQUIPMENT_OWNER = "equipment_owner"
    ADMIN = "admin"

    CHOICES = [
        (FARMER, "Farmer"),
        (BUYER, "Buyer"),
        (LABOUR, "Labour"),
        (EQUIPMENT_OWNER, "Equipment Owner"),
        (ADMIN, "Admin"),
    ]

    PHONE_AUTH_ROLES = {FARMER, LABOUR, EQUIPMENT_OWNER}
    EMAIL_AUTH_ROLES = {BUYER}


# ---- Job Status ----
class JobStatus:
    OPEN = "open"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    CHOICES = [
        (OPEN, "Open"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]


# ---- Booking Status ----
class BookingStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_USE = "in_use"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (IN_USE, "In Use"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]


# ---- Order Status ----
class OrderStatus:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
    ]


# ---- Notification Types ----
class NotificationType:
    BUYER_INTERESTED = "buyer_interested"
    EQUIPMENT_BOOKED = "equipment_booked"
    LABOUR_ACCEPTED = "labour_accepted"
    MARKETPLACE_UPDATE = "marketplace_update"
    WEATHER_ALERT = "weather_alert"
    NEW_MESSAGE = "new_message"
    JOB_POSTED = "job_posted"
    ORDER_UPDATE = "order_update"
    GENERAL = "general"

    CHOICES = [
        (BUYER_INTERESTED, "Buyer Interested"),
        (EQUIPMENT_BOOKED, "Equipment Booked"),
        (LABOUR_ACCEPTED, "Labour Accepted"),
        (MARKETPLACE_UPDATE, "Marketplace Update"),
        (WEATHER_ALERT, "Weather Alert"),
        (NEW_MESSAGE, "New Message"),
        (JOB_POSTED, "Job Posted"),
        (ORDER_UPDATE, "Order Update"),
        (GENERAL, "General"),
    ]


# ---- Review Types ----
class ReviewType:
    FARMER = "farmer"
    BUYER = "buyer"
    LABOUR = "labour"
    EQUIPMENT = "equipment"
    PRODUCT = "product"

    CHOICES = [
        (FARMER, "Farmer"),
        (BUYER, "Buyer"),
        (LABOUR, "Labour"),
        (EQUIPMENT, "Equipment"),
        (PRODUCT, "Product"),
    ]


# ---- Equipment Categories ----
class EquipmentCategory:
    TRACTOR = "tractor"
    HARVESTER = "harvester"
    PLOUGH = "plough"
    SEEDER = "seeder"
    SPRAYER = "sprayer"
    IRRIGATION = "irrigation"
    THRESHER = "thresher"
    CULTIVATOR = "cultivator"
    OTHER = "other"

    CHOICES = [
        (TRACTOR, "Tractor"),
        (HARVESTER, "Harvester"),
        (PLOUGH, "Plough"),
        (SEEDER, "Seeder"),
        (SPRAYER, "Sprayer"),
        (IRRIGATION, "Irrigation"),
        (THRESHER, "Thresher"),
        (CULTIVATOR, "Cultivator"),
        (OTHER, "Other"),
    ]


# ---- Country Codes (Default India) ----
DEFAULT_COUNTRY_CODE = "+91"

SUPPORTED_COUNTRY_CODES = [
    ("+91", "India (+91)"),
    ("+1", "USA (+1)"),
    ("+44", "UK (+44)"),
    ("+61", "Australia (+61)"),
    ("+971", "UAE (+971)"),
]

# ---- Quantity Units ----
class QuantityUnit:
    KG = "kg"
    QUINTAL = "quintal"
    TON = "ton"
    PIECE = "piece"
    DOZEN = "dozen"
    BUNDLE = "bundle"
    BAG = "bag"

    CHOICES = [
        (KG, "Kilogram"),
        (QUINTAL, "Quintal"),
        (TON, "Ton"),
        (PIECE, "Piece"),
        (DOZEN, "Dozen"),
        (BUNDLE, "Bundle"),
        (BAG, "Bag"),
    ]
