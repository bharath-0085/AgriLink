# Agri Link — Production-Ready Django Backend

Agri Link is a scalable, modular, and production-ready backend platform built using Python 3.11+ and Django to connect **Farmers, Labourers, Buyers, and Equipment Owners**.

---

## 🛠 Tech Stack & Integrations

- **Backend**: Python 3.11+ & Django 5.x
- **Database**: MongoDB Atlas via official `django-mongodb-backend`
- **Authentication**: Firebase Authentication (Phone OTP) + Email & Password (with SMTP verification)
- **Cloud Storage**: Cloudinary for user profile pictures, crop images, and leaf scan files
- **Weather Services**: OpenWeather API (featuring custom geo-rounding coordinate caching)
- **AI Chatbot**: Google Gemini 2.5 API (restricted exclusively to agricultural topics)
- **AI Model Prediction**:
  - **Crop Recommendation**: Scikit-Learn Model (`crop_model.pkl`)
  - **Plant Leaf Disease Classification**: TensorFlow Keras Model (`best_model.keras`)

---

## 📂 Project Architecture & Apps

The codebase uses a clean, decoupling-focused structure with individual apps nested in the `apps/` directory:

1. **`core`**: Contains base abstract models, cross-app review/rating systems, token authentication middleware, reusable validators, customized DRF response envelopes, and global exception handlers.
2. **`accounts`**: Manages phone OTP verification (Firebase), buyer email sign-up/login, password resets, and user profile management.
3. **`farmer`**: Aggregates dashboard summaries, crop logs, and labour hiring/equipment rental stats.
4. **`buyer`**: Supports crop catalog browsing, searching, and filtering.
5. **`labour`**: Handles labour profiles, wage listings, and daily job hiring (accepting/rejecting).
6. **`equipment`**: Manages equipment listing (tractor, cultivator, harvester), pricing, and rental bookings.
7. **`marketplace`**: Facilitates crop listings, ordering, order status tracking, and buyer bookmarking.
8. **`weather`**: Fetches weather metrics with geographical rounding caching (30-minute TTL) to minimize external API costs.
9. **`chat`**: Handles secure private conversation rooms, real-time message tracking, and image sharing.
10. **`notification`**: Central system for user alert routing (new order, booking confirmation, weather alerts).
11. **`ai_module`**: Singletons to load models lazily, pre-process raw input metrics or leaf images, and process Gemini chatbot agriculture-only instructions.
12. **`adminpanel`**: An admin dashboard located at a hidden URL (`/admin-login/`) displaying platform-wide statistics.

---

## ⚙️ Setup & Installation Instructions

### 1. Prerequisites
- Python 3.11 or later
- MongoDB Atlas cluster URL
- Firebase project credentials file (`firebase-service-account.json`)
- API keys for OpenWeather, Cloudinary, and Gemini

### 2. Installation
Clone the repository, then initialize a Python virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```

Ensure your `firebase-service-account.json` file is placed in the root directory.

### 4. Database Setup & Migrations
Sync your database schemas with MongoDB Atlas:
```bash
python manage.py migrate
```

Create a superuser for admin panel access:
```bash
python manage.py createsuperuser
```

### 5. Running the Server
```bash
python manage.py runserver
```
The backend API will be available at `http://127.0.0.1:8000/`.

---

## 🛰 API Endpoints Documentation (v1)

### 🔑 Authentication (`/api/v1/accounts/`)
- `POST /register/phone/`: Verify Firebase phone token, create farmer/labourer.
- `POST /register/email/`: Register buyer with email + password (sends verification email).
- `POST /verify-email/`: Confirm buyer's email token.
- `POST /login/phone/`: Authenticate farmer/labourer using Firebase token.
- `POST /login/email/`: Authenticate buyer using email and password.
- `POST /forgot-password/`: Request password reset token.
- `POST /reset-password/`: Update password using email token.
- `GET/PUT /profile/`: Retrieve or update user details.
- `POST /profile/photo/`: Upload profile picture to Cloudinary.
- `POST /logout/`: Invalidate active session token.

### 🚜 Farmer & Buyer Dashboards
- `GET /api/v1/farmer/dashboard/`: Farmer statistics summary.
- `GET /api/v1/buyer/dashboard/`: Buyer purchases and bookmarks summary.

### 🌾 Marketplace & Orders (`/api/v1/marketplace/`)
- `GET /`: Browse crops with pagination, search, price ranges, and location filters.
- `POST /`: Farmer uploads crop listings (with image uploads to Cloudinary).
- `GET /<id>/`: Detail view of a crop listing.
- `POST /<id>/order/`: Buyer places an order for a crop quantity.
- `GET /orders/`: List orders (farmer sales or buyer purchases).
- `POST /orders/<id>/action/`: Update order status (`confirm`, `cancel`, `ship`, `deliver`).
- `GET/POST /bookmarks/`: Add, remove, or list crop bookmarks.
- `GET /nearby/`: Search for nearby farmers or buyers.

### ⚙️ Equipment Rental (`/api/v1/equipment/`)
- `GET/POST /`: List or upload equipment rental listings.
- `GET/PUT/DELETE /<id>/`: CRUD for an equipment listing.
- `POST /<id>/book/`: Book equipment for a time duration (calculates hourly or daily cost).
- `GET /bookings/`: List rentals (owner listings or renter bookings).
- `POST /bookings/<booking_id>/action/`: Update rental booking status (`confirm`, `cancel`, `complete`).
- `GET /nearby/`: Search for nearby rental listings based on GPS.

### 🔨 Labour Hiring (`/api/v1/labour/`)
- `GET/POST /profile/`: Get or update labour skill, wage, and experience details.
- `GET /jobs/`: List available jobs (labourers) or posted jobs (farmers).
- `POST /jobs/create/`: Farmer posts a new work requirement.
- `POST /jobs/<id>/accept/`: Labourer accepts a job posting.
- `POST /jobs/<id>/reject/`: Labourer cancels/rejects an accepted job.
- `GET /jobs/history/`: List completed or past jobs.
- `GET /nearby/`: Locate nearby labourers.

### 🌤 Weather & Navigation
- `GET /api/v1/weather/current/?lat=X&lng=Y`: Returns temperature, humidity, wind speed, and rain probability using coordinate-based caching.

### 💬 Private Chat Room (`/api/v1/chat/`)
- `GET/POST /rooms/`: List active rooms or open/create a room with another user.
- `GET /rooms/<room_id>/messages/`: Fetch message history.
- `POST /rooms/<room_id>/messages/`: Send text or image messages.
- `POST /rooms/<room_id>/read/`: Mark room conversations as read.

### 🔔 System Alerts (`/api/v1/notifications/`)
- `GET /`: Get all notifications.
- `GET /unread-count/`: Get number of unread notifications.
- `POST /<id>/read/`: Mark a specific notification as read.
- `POST /read-all/`: Mark all notifications as read.

### 🤖 AI Services (`/api/v1/ai/`)
- `POST /crop-recommend/`: Receives N, P, K, pH, temp, humidity, rainfall metrics and returns recommended crops.
- `POST /disease-detect/`: Receives a leaf image upload, processes it, and returns plant disease classification alongside detailed treatments and prevention instructions.
- `POST /chatbot/`: Handles natural language queries. System guidelines prompt Gemini 2.5 to answer agriculture-only topics and politely turn away unrelated questions.

### 👑 Admin Portal (`/admin-login/`)
- `POST /login/`: Admin login view.
- `GET /dashboard/`: Platform overview dashboard presenting total users, listings, bookings, and active orders.

---

## 🔒 Security Practices

1. **Decoupled Configuration**: All keys, DB URIs, and authentication settings are strictly loaded from environment variables (`.env`).
2. **Input Validation**: All incoming REST payloads are strictly verified via Django REST serializers before executing database mutations.
3. **Password Security**: Buyer and admin passwords are securely hashed using PBKDF2/Argon2.
4. **Token Security**: REST endpoints require an active `Authorization: Token <key>` header validated against a TTL-expiring token store.
5. **Polite Chatbot Constraints**: System configuration guards Gemini API prompts against malicious jailbreaking and off-topic conversations.
