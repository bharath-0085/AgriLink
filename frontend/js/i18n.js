/**
 * Agri Link — Pure Additive Multilanguage Translation Layer (i18n)
 * Supports: English (en) & Tamil (ta)
 */

(function () {
    'use strict';

    const TRANSLATIONS = {
        en: {
        "sidebar": {
                "dashboard": "Dashboard",
                "crop_recommendation": "Crop Recommendation",
                "disease_detection": "Disease Detection",
                "labour_hiring": "Labour Hiring",
                "equipment_rental": "Equipment Rental",
                "marketplace": "Marketplace",
                "my_bookings": "My Bookings",
                "my_sales": "My Sales",
                "weather_alerts": "Weather & Alerts",
                "ai_assistant": "AI Assistant",
                "settings": "Settings",
                "help_support": "Help & Support",
                "logout": "Logout"
        },
        "header": {
                "welcome_back": "Welcome back",
                "subtitle": "Here's what's happening in your farm today.",
                "detecting_location": "Detecting location...",
                "farmer_role": "Farmer",
                "joined": "Joined:",
                "edit_profile": "Edit Profile",
                "logout": "Logout",
                "lang_toggle_en": "EN",
                "lang_toggle_ta": "தமிழ்",
                "sub_overview": "Here's what's happening in your farm today.",
                "sub_crop_rec": "Enter soil and climate metrics to predict optimal crop yields.",
                "sub_disease": "Upload leaf photo to run machine learning symptom check.",
                "sub_labour": "Find and hire local agricultural workers with daily wages.",
                "sub_equipment": "Rent high-quality agricultural machinery and tools.",
                "sub_marketplace": "Sell crops directly to buyers and check your transactions.",
                "sub_bookings": "Track your scheduled labourers and equipment bookings.",
                "sub_sales": "Track crop revenue and historical transactions.",
                "sub_weather": "Realtime farm weather forecast and advisory alerts.",
                "sub_assistant": "Chat with Agri Link AI farming assistant bot.",
                "sub_settings": "Manage system preferences and profile parameters.",
                "sub_help": "Reach out to helpline operators or view support documentation."
        },
        "overview": {
                "crop_health_score": "Crop Health Score",
                "good_condition": "Good Condition",
                "labour_bookings": "Labour Bookings",
                "active_bookings": "Active Bookings",
                "equipment_bookings": "Equipment Bookings",
                "upcoming": "Upcoming",
                "marketplace_orders": "Marketplace Orders",
                "new_interested_buyers": "New Interested Buyers",
                "total_earnings": "Total Earnings",
                "this_month": "This Month",
                "farm_map_title": "Interactive Farm Map & Geocoding",
                "auto_detect_gps": "Auto-Detect My Location",
                "geo_coords_title": "Geographic Coordinates",
                "latitude": "Latitude:",
                "longitude": "Longitude:",
                "village_area": "Village / Area:",
                "district": "District:",
                "state": "State:",
                "reverse_geo_notice": "Reverse geocoding resolves coordinates to actual villages using Nominatim.",
                "banner_title": "Get AI Powered Crop Recommendation",
                "banner_desc": "Get the best crop suggestions for higher yield and profit based on soil parameters.",
                "get_recommendation": "Get Recommendation",
                "upcoming_bookings_title": "Upcoming Bookings",
                "view_all": "View All",
                "labour_harvesting": "Labour — Harvesting",
                "confirmed": "Confirmed",
                "tractor_land_prep": "Tractor — Land Prep",
                "scheduled": "Scheduled",
                "recent_activities": "Recent Activities",
                "act_tomatoes_listed": "You listed 100 kg of Tomatoes for sale.",
                "act_buyers_interest": "2 new buyers showed interest in your Tomatoes.",
                "act_disease_scanned": "Disease detection completed for your crop.",
                "quick_access": "Quick Access",
                "hire_labour": "Hire Labour",
                "rent_equipment": "Rent Equipment",
                "ai_tips_title": "AI Tips for You",
                "tip_of_day": "Tip of the Day",
                "tip_text": "Irrigate crops in the early morning to minimize water loss through evaporation."
        },
        "crop_rec": {
                "title": "Crop Recommendation Model",
                "nitrogen": "Nitrogen (N)",
                "phosphorus": "Phosphorus (P)",
                "potassium": "Potassium (K)",
                "ph": "Soil pH (0.0-14.0)",
                "temperature": "Temperature (°C)",
                "humidity": "Humidity (%)",
                "rainfall": "Rainfall (mm)",
                "btn_predict": "Get AI Prediction",
                "optimal_crop": "Optimal Crop",
                "confidence": "Confidence",
                "analysis_title": "Recommendation Analysis",
                "fertilizer": "Fertilizer",
                "season": "Season",
                "expected_yield": "Expected Yield"
        },
        "disease": {
                "title": "AI Crop Disease Scan",
                "take_photo": "Take Photo",
                "choose_gallery": "Choose from Gallery",
                "upload_or_take": "Upload or Take a Leaf Photo",
                "upload_hint": "Supports JPG, PNG, and WEBP formats (Max 10MB)",
                "remove_image": "Remove Image",
                "change_image": "Change Image",
                "btn_scan": "Scan Leaf",
                "scanning": "Scanning Leaf...",
                "detection_result": "Detection Result",
                "suggested_treatment": "Suggested Treatment",
                "prevention": "Prevention"
        },
        "labour": {
                "title": "Agricultural Labour Hiring",
                "subtitle": "Directly hire verified agricultural workers for harvesting, plowing, planting, and seasonal operations.",
                "available_workers": "Available Workers",
                "daily_wages_badge": "Transparent Daily Wages",
                "direct_hiring_badge": "100% Direct Hiring",
                "hire_alert_title": "Hire Request Confirmed!",
                "hire_alert_msg": "Worker has been notified. You can track this in your Bookings tab.",
                "search_placeholder": "Search by worker name, skill, or town...",
                "skill_label": "Skill / Specialty",
                "all_skills": "All Skills",
                "location_label": "Location",
                "all_locations": "All Locations",
                "wage_range_label": "Daily Wage",
                "all_wages": "All Wages",
                "per_day": "/ day",
                "experience": "Experience",
                "hire_now": "Hire Now",
                "call_worker": "Call"
        },
        "equipment": {
                "title": "Equipment Rental",
                "subtitle": "Find and rent agricultural machinery near you",
                "verified_owners": "Verified Owners",
                "insured": "Insured",
                "search_label": "Search Equipment",
                "search_placeholder": "e.g. Tractor, Sprayer, JCB, owner...",
                "type_label": "Equipment Type",
                "all_types": "All Types",
                "location_label": "Location",
                "all_locations": "All Locations",
                "availability_label": "Availability",
                "all_availability": "All Availability",
                "available_now": "Available Now",
                "unavailable": "Rented Out / Unavailable",
                "max_rate_label": "Max Daily Rate",
                "all_rates": "All Rates",
                "sort_label": "Sort By",
                "sort_default": "Default / Recommended",
                "btn_filter": "Filter",
                "btn_clear": "Clear",
                "book_now": "Book Now",
                "contact_owner": "Contact Owner"
        },
        "marketplace": {
                "title": "Crop Marketplace",
                "subtitle": "Sell your harvest directly to buyers or browse market demands",
                "btn_list_crop": "List Your Crop",
                "my_active_listings": "My Active Listings",
                "available_market": "Available Market Listings",
                "search_crops": "Search Crops",
                "search_placeholder": "e.g. Wheat, Rice, Tomato...",
                "location": "Location",
                "any_location": "Any Location",
                "category": "Crop Category",
                "all_categories": "All Categories",
                "quantity": "Quantity",
                "price": "Price",
                "edit": "Edit",
                "remove": "Remove",
                "contact_buyer": "Contact Buyer",
                "verified_buyer": "Verified Buyer",
                "interested_in": "Interested In:",
                "phone": "Phone:",
                "call_now": "Call Now"
        },
        "bookings": {
                "title": "My Bookings",
                "subtitle": "Manage your hired labour and rented machinery",
                "labour_bookings": "Labour Bookings",
                "equipment_bookings": "Equipment Bookings",
                "loading_labour": "Loading labour bookings...",
                "loading_equipment": "Loading equipment bookings...",
                "status_confirmed": "Confirmed",
                "status_pending": "Pending",
                "status_completed": "Completed",
                "status_cancelled": "Cancelled"
        },
        "sales": {
                "title": "Sales Reports",
                "subtitle": "Sales logs and financial earnings details appear here.",
                "total_revenue": "Total Revenue",
                "total_orders": "Total Orders",
                "avg_order_value": "Avg. Order Value",
                "completed_sales": "Completed Sales",
                "revenue_chart_title": "Monthly Revenue Trend",
                "crop_breakdown_title": "Crop Sales Distribution",
                "transaction_history": "Transaction History",
                "btn_export_csv": "Export CSV",
                "btn_export_pdf": "Export PDF",
                "th_order_id": "Order ID",
                "th_date": "Date",
                "th_crop": "Crop",
                "th_buyer": "Buyer",
                "th_qty": "Quantity",
                "th_price": "Price",
                "th_total": "Total Amount",
                "th_status": "Status",
                "th_actions": "Actions",
                "pending_payments": "Pending Payments",
                "top_selling_crop": "Top Selling Crop",
                "revenue_overview": "Revenue Overview",
                "earnings_trend": "Your earnings trend over time.",
                "sales_by_crop": "Sales by Crop",
                "sales_by_crop_sub": "Revenue distribution across harvested crops.",
                "weekly": "Weekly",
                "monthly": "Monthly",
                "yearly": "Yearly",
                "showing_info": "Showing",
                "previous": "Previous",
                "next": "Next",
                "receipt_title": "Sale Order Receipt"
        },
        "weather": {
                "title": "Weather & Agricultural Advisories",
                "subtitle": "Real-time micrometeorology, multi-day agricultural forecast, and actionable field advisories for your crops.",
                "live_feed": "Live Weather Feed",
                "btn_gps": "Use My GPS",
                "btn_refresh": "Refresh Data",
                "search_placeholder": "Search District or Town (e.g. Salem, Madurai)...",
                "btn_search": "Search",
                "quick_regions": "Quick Regions:",
                "updating_data": "Updating Farm Weather Data...",
                "updating_desc": "Fetching satellite radar and agricultural advisories.",
                "humidity": "Humidity",
                "wind_speed": "Wind Speed",
                "rainfall": "Rainfall",
                "forecast_7day": "5–7 Day Agro Forecast",
                "agri_advisory": "Agricultural Advisory",
                "hourly_forecast": "Hourly Agricultural Forecast (Next 24 Hours)",
                "hourly_sub": "Field operations timeline, temperature curve & precipitation chances",
                "radar_intervals": "3-Hour Radar Intervals",
                "days_forecast": "5–7 Day Agro Forecast",
                "days_sub": "Daily temperature extremes, rain probability & relative humidity",
                "advisories_title": "Actionable Farmer Advisories & Alerts",
                "advisories_sub": "Targeted crop management guidelines derived from current weather hazards",
                "all_advisories": "All Advisories",
                "pressure": "Pressure",
                "visibility": "Visibility",
                "operations": "Operations",
                "optimal_window": "Optimal Window",
                "safe_spraying": "Safe Spraying"
        },
        "assistant": {
                "title": "AI Assistant",
                "subtitle": "Get expert farming advice, crop guidance and solutions to your agricultural problems.",
                "happy_farming": "Happy Farming!",
                "online": "Online",
                "card_title": "AI Farming Assistant",
                "card_subtitle": "Specialized in Indian agronomy, crop protection & fertilizer schedules",
                "clear_chat": "Clear Chat",
                "chip_paddy": "🌾 Best NPK ratio for paddy?",
                "chip_blight": "🍅 Tomato early blight treatment?",
                "chip_scheme": "🏛️ PM-KISAN scheme eligibility?",
                "chip_spacing": "🌽 Cotton pest management & spacing?",
                "input_placeholder": "Ask anything about farming, crops, fertilizer, pests...",
                "btn_send": "Send",
                "thinking": "Agri Link AI is thinking...",
                "disclaimer": "AI recommendations are for advisory guidance. Verify critical pesticide decisions with local agricultural extension officers."
        },
        "settings": {
                "profile_title": "Profile Settings",
                "profile_subtitle": "Edit names, locations, and system configuration profiles.",
                "photo_heading": "Farm Profile Photo",
                "photo_sub": "Upload a clear photo or farm logo (JPG, PNG up to 5MB).",
                "change_photo": "Change Photo",
                "full_name": "Full Name",
                "phone": "Phone Number",
                "email": "Email Address",
                "village": "Location / Village",
                "district": "District",
                "state": "State",
                "pincode": "Pincode",
                "pref_lang": "Preferred Language",
                "farm_size": "Farm Size (Acres)",
                "primary_crops": "Primary Crops Grown",
                "btn_save_profile": "Save Profile Changes",
                "notif_title": "Notification Preferences",
                "notif_subtitle": "Choose how you want to be updated.",
                "weather_alerts": "Weather & Storm Alerts",
                "disease_alerts": "Crop Disease Outbreak Warnings",
                "market_price_alerts": "Market Price Fluctuations",
                "scheme_alerts": "Govt. Scheme & Subsidy Announcements",
                "order_alerts": "Order & Booking Updates",
                "toast_success": "Success",
                "profile_updated": "Profile updated successfully!",
                "toast_error": "Error",
                "account_security": "Account & Security",
                "app_preferences": "App Preferences",
                "danger_zone": "Danger Zone",
                "change_password": "Change Password",
                "two_factor": "Two-Factor Authentication (2FA)",
                "phone_verified": "Verified Phone Number",
                "save_changes": "Save Changes"
        },
        "help": {
                "title": "Help Desk Support",
                "subtitle": "Reach out to toll-free support or open tickets.",
                "call_toll_free": "Call Toll-Free",
                "call_now": "Call Now",
                "whatsapp_support": "WhatsApp Support",
                "chat_now": "Chat Now",
                "email_support": "Email Support",
                "send_mail": "Send Mail",
                "live_chat": "Live Chat",
                "start_chat": "Start Chat",
                "operating_hours": "Operating Hours: Available Mon–Sat, 8:00 AM – 8:00 PM. (Toll-Free & WhatsApp)",
                "support_active": "Support Active",
                "raise_ticket_title": "Raise a Support Ticket",
                "raise_ticket_sub": "Describe your issue and our team will get back to you.",
                "issue_category": "Issue Category",
                "subject": "Subject",
                "description": "Detailed Description",
                "btn_submit_ticket": "Submit Support Ticket",
                "my_tickets_title": "My Support Tickets",
                "faqs_title": "Frequently Asked Questions",
                "toast_ticket_submitted": "Support ticket submitted successfully!"
        },
        "modals": {
                "contact_buyer_title": "Contact Buyer",
                "contact_buyer_sub": "Get in touch to negotiate and finalize your sale",
                "list_crop_title": "List Your Crop",
                "list_crop_sub": "Provide details to sell your crop to buyers directly",
                "publish_listing": "Publish Listing",
                "edit_crop_title": "Edit Crop Listing",
                "edit_crop_sub": "Update your crop details",
                "save_changes": "Save Changes",
                "rent_equipment_title": "Rent Equipment",
                "rent_equipment_sub": "Select dates and confirm your booking",
                "confirm_rental": "Confirm Rental",
                "hire_worker_title": "Hire Agricultural Worker",
                "confirm_hire": "Confirm & Hire",
                "edit_profile_title": "Edit Farmer Profile"
        },
        "common": {
                "save": "Save",
                "cancel": "Cancel",
                "close": "Close",
                "loading": "Loading...",
                "search": "Search",
                "filter": "Filter",
                "clear": "Clear",
                "edit": "Edit",
                "delete": "Delete",
                "view": "View",
                "submit": "Submit"
        }
},
        ta: {
        "sidebar": {
                "dashboard": "முகப்பு பலகை",
                "crop_recommendation": "பயிர் பரிந்துரை",
                "disease_detection": "நோய் கண்டறிதல்",
                "labour_hiring": "விவசாயப் பணியாளர்கள்",
                "equipment_rental": "வேளாண் கருவிகள் வாடகை",
                "marketplace": "விவசாய சந்தை",
                "my_bookings": "எனது முன்பதிவுகள்",
                "my_sales": "எனது விற்பனை",
                "weather_alerts": "வானிலை & எச்சரிக்கைகள்",
                "ai_assistant": "ஏஐ வேளாண் உதவியாளர்",
                "settings": "அமைப்புகள்",
                "help_support": "உதவி & ஆதரவு",
                "logout": "வெளியேறு"
        },
        "header": {
                "welcome_back": "மீண்டும் வருக",
                "subtitle": "இன்று உங்கள் பண்ணையில் என்ன நடக்கிறது என்பதை இங்கே காண்க.",
                "detecting_location": "இருப்பிடத்தைக் கண்டறிகிறது...",
                "farmer_role": "விவசாயி",
                "joined": "சேர்ந்த நாள்:",
                "edit_profile": "சுயவிவரத்தைத் திருத்து",
                "logout": "வெளியேறு",
                "lang_toggle_en": "EN",
                "lang_toggle_ta": "தமிழ்",
                "sub_overview": "இன்று உங்கள் பண்ணையில் என்ன நடக்கிறது என்பதை இங்கே காண்க.",
                "sub_crop_rec": "மண் மற்றும் காலநிலை அளவீடுகளை உள்ளிட்டு சிறந்த பயிர் விளைச்சலை கணிக்கவும்.",
                "sub_disease": "இலை புகைப்படத்தைப் பதிவேற்றி இயந்திர கற்றல் மூலம் நோய் அறிகுறிகளை கண்டறியவும்.",
                "sub_labour": "தினசரி கூலி அடிப்படையில் உள்ளூர் விவசாய பணியாளர்களைத் தேடி பணியமர்த்தவும்.",
                "sub_equipment": "உயர்தர விவசாய இயந்திரங்கள் மற்றும் கருவிகளை வாடகைக்கு எடுக்கவும்.",
                "sub_marketplace": "விளைச்சலை நேரடியாக வாங்குபவர்களுக்கு விற்று பரிவர்த்தனைகளை கண்காணிக்கவும்.",
                "sub_bookings": "பதிவு செய்யப்பட்ட தொழிலாளர்கள் மற்றும் இயந்திர வாடகை அட்டவணைகளை கண்காணிக்கவும்.",
                "sub_sales": "பயிர் வருவாய் மற்றும் முந்தைய விற்பனை வரலாற்றை கண்காணிக்கவும்.",
                "sub_weather": "நேரலை பண்ணை வானிலை முன்னறிவிப்பு மற்றும் வேளாண் எச்சரிக்கைகள்.",
                "sub_assistant": "அக்ரி லிங்க் ஏஐ விவசாய உதவியாளருடன் உரையாடவும்.",
                "sub_settings": "அமைப்பு விருப்பத்தேர்வுகள் மற்றும் சுயவிவர அமைப்புகளை நிர்வகிக்கவும்.",
                "sub_help": "உதவி மையத்தை தொடர்பு கொள்ளவும் அல்லது ஆதரவு ஆவணங்களை படிக்கவும்."
        },
        "overview": {
                "crop_health_score": "பயிர் ஆரோக்கிய மதிப்பீடு",
                "good_condition": "நல்ல நிலை",
                "labour_bookings": "பணியாளர் முன்பதிவுகள்",
                "active_bookings": "செயலில் உள்ள முன்பதிவுகள்",
                "equipment_bookings": "கருவிகள் முன்பதிவு",
                "upcoming": "வரவிருக்கும்",
                "marketplace_orders": "சந்தை ஆர்டர்கள்",
                "new_interested_buyers": "புதிய ஆர்வமுள்ள வாங்குபவர்கள்",
                "total_earnings": "மொத்த வருவாய்",
                "this_month": "இந்த மாதம்",
                "farm_map_title": "ஊடாடும் பண்ணை வரைபடம் & புவிக்குறியீடு",
                "auto_detect_gps": "எனது இருப்பிடத்தைக் கண்டறி",
                "geo_coords_title": "புவியியல் ஆயத்தொலைவுகள்",
                "latitude": "அட்சரேகை (Latitude):",
                "longitude": "தீர்க்கரேகை (Longitude):",
                "village_area": "கிராமம் / பகுதி:",
                "district": "மாவட்டம்:",
                "state": "மாநிலம்:",
                "reverse_geo_notice": "நோமினேடிம் (Nominatim) மூலம் உண்மையான கிராமப் பெயர்கள் கண்டறியப்படுகின்றன.",
                "banner_title": "ஏஐ பயிர் பரிந்துரையைப் பெறுங்கள்",
                "banner_desc": "மண் வள அளவுகளின் அடிப்படையில் அதிக மகசூல் மற்றும் லாபம் தரும் சிறந்த பயிர்களைத் தேர்ந்தெடுக்கவும்.",
                "get_recommendation": "பரிந்துரை பெறுக",
                "upcoming_bookings_title": "வரவிருக்கும் முன்பதிவுகள்",
                "view_all": "அனைத்தையும் காண்க",
                "labour_harvesting": "பணியாளர் — அறுவடை",
                "confirmed": "உறுதிசெய்யப்பட்டது",
                "tractor_land_prep": "டிராக்டர் — உழவுப் பணி",
                "scheduled": "திட்டமிடப்பட்டது",
                "recent_activities": "சமீபத்திய செயல்பாடுகள்",
                "act_tomatoes_listed": "விற்பனைக்காக 100 கிலோ தக்காளி பட்டியலிடப்பட்டது.",
                "act_buyers_interest": "உங்கள் தக்காளியை வாங்க 2 புதிய வாங்குபவர்கள் ஆர்வம் காட்டியுள்ளனர்.",
                "act_disease_scanned": "உங்கள் பயிரின் நோய் கண்டறிதல் வெற்றிகரமாக முடிந்தது.",
                "quick_access": "விரைவு அணுகல்",
                "hire_labour": "பணியாளர்களை அமர்த்துக",
                "rent_equipment": "கருவிகள் வாடகைக்கு எடுக்க",
                "ai_tips_title": "உங்களுக்கான ஏஐ குறிப்புகள்",
                "tip_of_day": "இன்றைய விவசாயக் குறிப்பு",
                "tip_text": "ஆவியாதல் மூலம் நீர் வீணாவதைத் தடுக்க அதிகாலையில் பயிர்களுக்குப் பாசனம் செய்யுங்கள்."
        },
        "crop_rec": {
                "title": "ஏஐ பயிர் பரிந்துரை மாதிரி",
                "nitrogen": "தழைச்சத்து (Nitrogen - N)",
                "phosphorus": "மணிச்சத்து (Phosphorus - P)",
                "potassium": "சாம்பல் சத்து (Potassium - K)",
                "ph": "மண் கார அமிலத்தன்மை (pH 0.0-14.0)",
                "temperature": "வெப்பநிலை (°C)",
                "humidity": "ஈரப்பதம் (%)",
                "rainfall": "மழைப்பொழிவு (மி.மீ)",
                "btn_predict": "ஏஐ பரிந்துரை பெறுக",
                "optimal_crop": "பொருத்தமான பயிர்",
                "confidence": "நம்பகத்தன்மை",
                "analysis_title": "பரிந்துரை பகுப்பாய்வு",
                "fertilizer": "உர மேலாண்மை",
                "season": "பருவம்",
                "expected_yield": "எதிர்பார்க்கப்படும் மகசூல்"
        },
        "disease": {
                "title": "ஏஐ பயிர் நோய் கண்டறிதல்",
                "take_photo": "புகைப்படம் எடு",
                "choose_gallery": "கேலரியிலிருந்து தேர்வு செய்",
                "upload_or_take": "இலையின் புகைப்படத்தைப் பதிவேற்றவும் அல்லது எடுக்கவும்",
                "upload_hint": "JPG, PNG, WEBP வடிவங்களை ஆதரிக்கிறது (அதிகபட்சம் 10MB)",
                "remove_image": "படத்தை நீக்கு",
                "change_image": "படத்தை மாற்று",
                "btn_scan": "இலையை ஸ்கேன் செய்க",
                "scanning": "இலை ஸ்கேன் செய்யப்படுகிறது...",
                "detection_result": "கண்டறியப்பட்ட முடிவு",
                "suggested_treatment": "பரிந்துரைக்கப்பட்ட சிகிச்சை",
                "prevention": "தடுப்பு முறைகள்"
        },
        "labour": {
                "title": "விவசாயப் பணியாளர்கள் தேர்வு",
                "subtitle": "அறுவடை, உழவு, நடுவு மற்றும் பருவகால பணிகளுக்கு சரிபார்க்கப்பட்ட விவசாயத் தொழிலாளர்களை நேரடியாக அமர்த்துங்கள்.",
                "available_workers": "கிடைக்கும் பணியாளர்கள்",
                "daily_wages_badge": "வெளிப்படையான தினசரி கூலி",
                "direct_hiring_badge": "100% நேரடி நியமனம்",
                "hire_alert_title": "பணி நியமனக் கோரிக்கை உறுதி செய்யப்பட்டது!",
                "hire_alert_msg": "பணியாளருக்குத் தகவல் தெரிவிக்கப்பட்டுள்ளது. எனது முன்பதிவுகள் பக்கத்தில் கண்காணிக்கலாம்.",
                "search_placeholder": "பணியாளர் பெயர், திறன் அல்லது ஊர் மூலம் தேடுங்கள்...",
                "skill_label": "திறன் / பணி வகை",
                "all_skills": "அனைத்து திறன்களும்",
                "location_label": "இருப்பிடம்",
                "all_locations": "அனைத்து இடங்களும்",
                "wage_range_label": "தினசரி கூலி",
                "all_wages": "அனைத்து கூலி விகிதங்களும்",
                "per_day": "/ நாள்",
                "experience": "அனுபவம்",
                "hire_now": "பணிக்கு அமர்த்துக",
                "call_worker": "அழைக்கவும்"
        },
        "equipment": {
                "title": "வேளாண் கருவிகள் வாடகை",
                "subtitle": "உங்கள் பகுதிக்கு அருகிலுள்ள விவசாய இயந்திரங்களைக் கண்டறிந்து வாடகைக்கு எடுங்கள்",
                "verified_owners": "சரிபார்க்கப்பட்ட உரிமையாளர்கள்",
                "insured": "காப்பீடு செய்யப்பட்டது",
                "search_label": "கருவிகளைத் தேடுக",
                "search_placeholder": "உதா: டிராக்டர், தெளிப்பான், ஜேசிபி...",
                "type_label": "கருவி வகை",
                "all_types": "அனைத்து வகைகள்",
                "location_label": "இருப்பிடம்",
                "all_locations": "அனைத்து இடங்களும்",
                "availability_label": "இருப்பு நிலை",
                "all_availability": "அனைத்து நிலைகளும்",
                "available_now": "தற்போது தயார்",
                "unavailable": "வாடகையில் உள்ளது / கிடைக்கவில்லை",
                "max_rate_label": "அதிகபட்ச தினசரி கட்டணம்",
                "all_rates": "அனைத்து கட்டணங்களும்",
                "sort_label": "வரிசைப்படுத்து",
                "sort_default": "பரிந்துரைக்கப்பட்டவை",
                "btn_filter": "வடிகட்டுக",
                "btn_clear": "நீக்குக",
                "book_now": "முன்பதிவு செய்க",
                "contact_owner": "உரிமையாளரைத் தொடர்பு கொள்க"
        },
        "marketplace": {
                "title": "விவசாய சந்தை",
                "subtitle": "உங்கள் விளைச்சலை இடைத்தரகரின்றி வாங்குபவர்களிடம் நேரடியாக விற்று நல்ல லாபம் பெறுங்கள்",
                "btn_list_crop": "பயிரைப் பட்டியலிடுக",
                "my_active_listings": "எனது நேரடிப் பட்டியல்கள்",
                "available_market": "சந்தையில் உள்ள தேவைகள்",
                "search_crops": "பயிர்களைத் தேடுக",
                "search_placeholder": "உதா: கோதுமை, நெல், தக்காளி...",
                "location": "இருப்பிடம்",
                "any_location": "எந்த இடமும்",
                "category": "பயிர் வகை",
                "all_categories": "அனைத்து பயிர் வகைகள்",
                "quantity": "அளவு",
                "price": "விலை",
                "edit": "திருத்து",
                "remove": "நீக்கு",
                "contact_buyer": "வாங்குபவரைத் தொடர்பு கொள்க",
                "verified_buyer": "சரிபார்க்கப்பட்ட வாங்குபவர்",
                "interested_in": "தேவைப்படும் பயிர்:",
                "phone": "தொலைபேசி:",
                "call_now": "அழைக்கவும்"
        },
        "bookings": {
                "title": "எனது முன்பதிவுகள்",
                "subtitle": "நீங்கள் அமர்த்திய தொழிலாளர்கள் மற்றும் வாடகைக்கு எடுத்த இயந்திரங்களை நிர்வகியுங்கள்",
                "labour_bookings": "பணியாளர் முன்பதிவுகள்",
                "equipment_bookings": "கருவிகள் முன்பதிவு",
                "loading_labour": "பணியாளர் முன்பதிவுகள் ஏற்றப்படுகின்றன...",
                "loading_equipment": "கருவிகள் முன்பதிவுகள் ஏற்றப்படுகின்றன...",
                "status_confirmed": "உறுதி செய்யப்பட்டது",
                "status_pending": "காத்திருப்பில் உள்ளது",
                "status_completed": "நிறைவடைந்தது",
                "status_cancelled": "ரத்து செய்யப்பட்டது"
        },
        "sales": {
                "title": "விற்பனை அறிக்கைகள்",
                "subtitle": "உங்கள் விற்பனைப் பதிவுகள் மற்றும் நிதி வருவாய் விவரங்கள் இங்கே தோன்றும்.",
                "total_revenue": "மொத்த வருமானம்",
                "total_orders": "மொத்த ஆர்டர்கள்",
                "avg_order_value": "சராசரி ஆர்டர் மதிப்பு",
                "completed_sales": "முடிவுற்ற விற்பனைகள்",
                "revenue_chart_title": "மாதாந்திர வருவாய் போக்கு",
                "crop_breakdown_title": "பயிர் வாரியான விற்பனைப் பகிர்வு",
                "transaction_history": "பரிவர்த்தனை வரலாறு",
                "btn_export_csv": "CSV பதிவிறக்கம்",
                "btn_export_pdf": "PDF பதிவிறக்கம்",
                "th_order_id": "ஆர்டர் எண்",
                "th_date": "தேதி",
                "th_crop": "பயிர்",
                "th_buyer": "வாங்குபவர்",
                "th_qty": "அளவு",
                "th_price": "விலை",
                "th_total": "மொத்தத் தொகை",
                "th_status": "நிலை",
                "th_actions": "செயல்கள்",
                "pending_payments": "நிலுவைத் தொகைகள்",
                "top_selling_crop": "அதிகம் விற்பனையான பயிர்",
                "revenue_overview": "வருவாய் கண்ணோட்டம்",
                "earnings_trend": "காலப்போக்கில் உங்கள் வருமானத்தின் போக்கு.",
                "sales_by_crop": "பயிர் வாரியான விற்பனை",
                "sales_by_crop_sub": "அறுவடை செய்யப்பட்ட பயிர்களின் வருவாய் பகிர்வு.",
                "weekly": "வாராந்திர",
                "monthly": "மாதாந்திர",
                "yearly": "வருடாந்திர",
                "showing_info": "காட்டப்படுகிறது",
                "previous": "முந்தையது",
                "next": "அடுத்தது",
                "receipt_title": "விற்பனை ரசீது"
        },
        "weather": {
                "title": "வானிலை & வேளாண் ஆலோசனைகள்",
                "subtitle": "நேரடி உள்ளூர் வானிலை, பல நாள் வேளாண் முன்னறிவிப்பு மற்றும் உங்கள் பயிர்களுக்கான கள ஆலோசனைகள்.",
                "live_feed": "நேரடி வானிலை தகவல்",
                "btn_gps": "எனது ஜிபிஎஸ் பயன்படுத்து",
                "btn_refresh": "புதுப்பிக்கவும்",
                "search_placeholder": "மாவட்டம் அல்லது ஊரைத் தேடுங்கள் (உதா: சேலம், மதுரை)...",
                "btn_search": "தேடுக",
                "quick_regions": "முக்கிய பகுதிகள்:",
                "updating_data": "பண்ணை வானிலை புதுப்பிக்கப்படுகிறது...",
                "updating_desc": "செயற்கைக்கோள் ரேடார் மற்றும் வேளாண் எச்சரிக்கைகள் பெறப்படுகின்றன.",
                "humidity": "ஈரப்பதம்",
                "wind_speed": "காற்றின் வேகம்",
                "rainfall": "மழைப்பொழிவு",
                "forecast_7day": "5–7 நாள் வேளாண் முன்னறிவிப்பு",
                "agri_advisory": "வேளாண் ஆலோசனை",
                "hourly_forecast": "மணிநேர வேளாண் முன்னறிவிப்பு (அடுத்த 24 மணிநேரம்)",
                "hourly_sub": "வயல்வெளி செயல்பாடுகள், வெப்பநிலை வளைவு & மழை வாய்ப்புகள்",
                "radar_intervals": "3-மணிநேர ரேடார் இடைவெளிகள்",
                "days_forecast": "5–7 நாள் வேளாண் முன்னறிவிப்பு",
                "days_sub": "தினசரி வெப்பநிலை உச்சங்கள், மழை சாத்தியக்கூறு & காற்றின் ஈரப்பதம்",
                "advisories_title": "விவசாயிகளுக்கான செயல் வழிகாட்டுதல்கள் & எச்சரிக்கைகள்",
                "advisories_sub": "தற்போதைய வானிலை ஆபத்துகளிலிருந்து பெறப்பட்ட இலக்கு பயிர் மேலாண்மை வழிகாட்டுதல்கள்",
                "all_advisories": "அனைத்து ஆலோசனைகள்",
                "pressure": "காற்றழுத்தம்",
                "visibility": "பார்வைத்திறன்",
                "operations": "செயல்பாடுகள்",
                "optimal_window": "ஏற்ற தருணம்",
                "safe_spraying": "பாதுகாப்பான தெளிப்பு"
        },
        "assistant": {
                "title": "ஏஐ வேளாண் உதவியாளர்",
                "subtitle": "நிபுணத்துவ விவசாய ஆலோசனைகள், பயிர் வழிகாட்டுதல் மற்றும் உங்கள் வேளாண் சிக்கல்களுக்கான தீர்வுகளைப் பெறுங்கள்.",
                "happy_farming": "மகிழ்ச்சியான விவசாயம்!",
                "online": "செயலில் உள்ளது",
                "card_title": "ஏஐ வேளாண்மை உதவியாளர்",
                "card_subtitle": "இந்திய வேளாண்மை, பயிர் பாதுகாப்பு & உர அட்டவணையில் சிறப்பானது",
                "clear_chat": "அரட்டையை அழிக்க",
                "chip_paddy": "🌾 நெல் பயிருக்கான சிறந்த NPK விகிதம் என்ன?",
                "chip_blight": "🍅 தக்காளி இலை கருகல் நோய்க்கான மருந்து?",
                "chip_scheme": "🏛️ பிஎம்-கிசான் (PM-KISAN) திட்டத் தகுதி?",
                "chip_spacing": "🌽 பருத்தி பூச்சி மேலாண்மை & இடைவெளி?",
                "input_placeholder": "விவசாயம், பயிர்கள், உரங்கள், பூச்சிகள் பற்றி எதையும் கேளுங்கள்...",
                "btn_send": "அனுப்புக",
                "thinking": "அக்ரி லிங்க் ஏஐ சிந்திக்கிறது...",
                "disclaimer": "ஏஐ பரிந்துரைகள் வழிகாட்டுதலுக்கானது மட்டுமே. முக்கியமான பூச்சிக்கொல்லி முடிவுகளை உள்ளூர் வேளாண் அலுவலரிடம் உறுதிப்படுத்தவும்."
        },
        "settings": {
                "profile_title": "சுயவிவர அமைப்புகள்",
                "profile_subtitle": "பெயர்கள், இருப்பிடங்கள் மற்றும் கணக்கு அமைப்புகளைத் திருத்தவும்.",
                "photo_heading": "பண்ணை சுயவிவரப் படம்",
                "photo_sub": "தெளிவான புகைப்படம் அல்லது பண்ணை லோகோவைப் பதிவேற்றவும் (JPG, PNG 5MB வரை).",
                "change_photo": "படத்தை மாற்று",
                "full_name": "முழு பெயர்",
                "phone": "தொலைபேசி எண்",
                "email": "மின்னஞ்சல் முகவரி",
                "village": "கிராமம் / ஊர்",
                "district": "மாவட்டம்",
                "state": "மாநிலம்",
                "pincode": "அஞ்சல் குறியீடு (Pincode)",
                "pref_lang": "விருப்பமான மொழி",
                "farm_size": "பண்ணை அளவு (ஏக்கர்)",
                "primary_crops": "பயிரிடப்படும் முக்கிய பயிர்கள்",
                "btn_save_profile": "சுயவிவர மாற்றங்களைச் சேமிக்கவும்",
                "notif_title": "அறிவிப்பு விருப்பத்தேர்வுகள்",
                "notif_subtitle": "தகவல்களை எவ்வாறு பெற விரும்புகிறீர்கள் என்பதைத் தேர்வுசெய்க.",
                "weather_alerts": "வானிலை & புயல் எச்சரிக்கைகள்",
                "disease_alerts": "பயிர் நோய் பரவல் எச்சரிக்கைகள்",
                "market_price_alerts": "சந்தை விலை ஏற்ற இறக்கங்கள்",
                "scheme_alerts": "அரசு மானியங்கள் & திட்ட அறிவிப்புகள்",
                "order_alerts": "ஆர்டர் & முன்பதிவு அறிவிப்புகள்",
                "toast_success": "வெற்றி",
                "profile_updated": "சுயவிவரம் வெற்றிகரமாகப் புதுப்பிக்கப்பட்டது!",
                "toast_error": "பிழை",
                "account_security": "கணக்கு & பாதுகாப்பு",
                "app_preferences": "செயலி விருப்பத்தேர்வுகள்",
                "danger_zone": "ஆபத்து மண்டலம் (Danger Zone)",
                "change_password": "கடவுச்சொல்லை மாற்று",
                "two_factor": "இருபடி சரிபார்ப்பு (2FA)",
                "phone_verified": "சரிபார்க்கப்பட்ட தொலைபேசி எண்",
                "save_changes": "மாற்றங்களைச் சேமிக்கவும்"
        },
        "help": {
                "title": "உதவி மையம் & ஆதரவு",
                "subtitle": "கட்டணமில்லா உதவி எண்ணைத் தொடர்பு கொள்ளவும் அல்லது புகார் மனு பதிவு செய்யவும்.",
                "call_toll_free": "கட்டணமில்லா அழைப்பு",
                "call_now": "அழைக்கவும்",
                "whatsapp_support": "வாட்ஸ்அப் உதவி",
                "chat_now": "அரட்டையடிக்க",
                "email_support": "மின்னஞ்சல் உதவி",
                "send_mail": "அஞ்சல் அனுப்புக",
                "live_chat": "நேரலை அரட்டை",
                "start_chat": "அரட்டையைத் தொடங்கு",
                "operating_hours": "செயல்படும் நேரம்: திங்கள்–சனி, காலை 8:00 – இரவு 8:00 வரை. (கட்டணமில்லா எண் & வாட்ஸ்அப்)",
                "support_active": "உதவி மையம் இயங்குகிறது",
                "raise_ticket_title": "புதிய உதவி மனு பதிவு செய்க",
                "raise_ticket_sub": "உங்கள் சிக்கலை விவரிக்கவும், எங்கள் குழு விரைவில் உங்களைத் தொடர்பு கொள்ளும்.",
                "issue_category": "பிரச்சனை வகை",
                "subject": "தலைப்பு",
                "description": "விரிவான விளக்கம்",
                "btn_submit_ticket": "மனுவைச் சமர்ப்பிக்கவும்",
                "my_tickets_title": "எனது உதவி மனுக்கள்",
                "faqs_title": "அடிக்கடி கேட்கப்படும் கேள்விகள் (FAQ)",
                "toast_ticket_submitted": "உதவி மனு வெற்றிகரமாகச் சமர்ப்பிக்கப்பட்டது!"
        },
        "modals": {
                "contact_buyer_title": "வாங்குபவரைத் தொடர்பு கொள்ளவும்",
                "contact_buyer_sub": "விலை பேசி விற்பனையை இறுதி செய்ய தொடர்பு கொள்ளவும்",
                "list_crop_title": "உங்கள் பயிரைப் பட்டியலிடுங்கள்",
                "list_crop_sub": "வாங்குபவர்களுக்கு நேரடியாக விற்க விவரங்களை வழங்கவும்",
                "publish_listing": "பயிரைப் பட்டியலிடுங்கள்",
                "edit_crop_title": "பயிர் பட்டியலைத் திருத்து",
                "edit_crop_sub": "உங்கள் பயிர் விவரங்களைப் புதுப்பிக்கவும்",
                "save_changes": "மாற்றங்களைச் சேமி",
                "rent_equipment_title": "இயந்திரத்தை வாடகைக்கு எடு",
                "rent_equipment_sub": "தேதிகளைத் தேர்ந்தெடுத்து உங்கள் முன்பதிவை உறுதிப்படுத்தவும்",
                "confirm_rental": "வாடகையை உறுதி செய்க",
                "hire_worker_title": "விவசாய பணியாளரை நியமிக்கவும்",
                "confirm_hire": "உறுதிசெய்து பணியமர்த்தவும்",
                "edit_profile_title": "விவசாயி சுயவிவரத்தைத் திருத்து"
        },
        "common": {
                "save": "சேமிக்க",
                "cancel": "ரத்து செய்க",
                "close": "மூடுக",
                "loading": "ஏற்றப்படுகிறது...",
                "search": "தேடுக",
                "filter": "வடிகட்டுக",
                "clear": "நீக்குக",
                "edit": "திருத்து",
                "delete": "நீக்கு",
                "view": "காண்க",
                "submit": "சமர்ப்பிக்க"
        }
}
    };

    function getStoredLang() {
        try {
            const saved = localStorage.getItem('userLanguage');
            if (saved && (saved.toLowerCase() === 'tamil' || saved.toLowerCase() === 'ta')) {
                return 'ta';
            }
        } catch (e) {
            console.warn('Unable to access localStorage for userLanguage:', e);
        }
        return 'en';
    }

    let currentLang = getStoredLang();

    // Dotted lookup helper: t('section.key', 'Fallback')
    function t(key, fallback = '') {
        if (!key) return fallback;
        const parts = key.split('.');
        let val = TRANSLATIONS[currentLang];
        for (let i = 0; i < parts.length; i++) {
            if (val && typeof val === 'object' && parts[i] in val) {
                val = val[parts[i]];
            } else {
                val = null;
                break;
            }
        }
        if (typeof val === 'string' && val.trim()) {
            return val;
        }
        // Fallback to English if currentLang is Tamil
        if (currentLang !== 'en') {
            let enVal = TRANSLATIONS.en;
            for (let i = 0; i < parts.length; i++) {
                if (enVal && typeof enVal === 'object' && parts[i] in enVal) {
                    enVal = enVal[parts[i]];
                } else {
                    enVal = null;
                    break;
                }
            }
            if (typeof enVal === 'string' && enVal.trim()) {
                return enVal;
            }
        }
        return fallback || key;
    }

    // Translate DOM elements
    function applyTranslations() {
        // Text contents
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            const translation = t(key);
            if (translation) {
                // If element has nested icon tag, preserve the first icon
                const icon = el.querySelector('i.bi, svg');
                if (icon && el.children.length === 1 && el.firstChild === icon) {
                    // Prepend icon, set text afterwards
                    el.childNodes.forEach(node => {
                        if (node.nodeType === Node.TEXT_NODE) {
                            node.textContent = ' ' + translation;
                        }
                    });
                } else {
                    el.textContent = translation;
                }
            }
        });

        // Placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            const translation = t(key);
            if (translation) {
                el.placeholder = translation;
            }
        });

        // Titles / Tooltips
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            const translation = t(key);
            if (translation) {
                el.title = translation;
            }
        });

        // Update Toggle buttons UI state
        updateToggleButtons();

        // Synchronize with Settings Select if exists
        const settingsSelect = document.getElementById('settings-language');
        if (settingsSelect) {
            settingsSelect.value = currentLang === 'ta' ? 'Tamil' : 'English';
        }
    }

    // Update Header Toggle button visuals
    function updateToggleButtons() {
        const btnEn = document.getElementById('lang-btn-en');
        const btnTa = document.getElementById('lang-btn-ta');
        if (btnEn && btnTa) {
            if (currentLang === 'ta') {
                btnEn.className = 'btn btn-sm rounded-pill px-2 py-0 fw-semibold text-secondary bg-transparent border-0';
                btnTa.className = 'btn btn-sm rounded-pill px-2 py-0 fw-bold btn-success text-white shadow-sm';
            } else {
                btnEn.className = 'btn btn-sm rounded-pill px-2 py-0 fw-bold btn-success text-white shadow-sm';
                btnTa.className = 'btn btn-sm rounded-pill px-2 py-0 fw-semibold text-secondary bg-transparent border-0';
            }
        }
    }

    // Switch language
    function changeLanguage(lang) {
        if (lang !== 'en' && lang !== 'ta') return;
        currentLang = lang;
        window.currentLanguage = lang;

        // Persist to localStorage matching Settings preference store
        try {
            localStorage.setItem('userLanguage', lang === 'ta' ? 'Tamil' : 'English');
        } catch (e) {
            console.warn('Unable to persist userLanguage to localStorage:', e);
        }

        // Apply DOM updates
        applyTranslations();

        // Dispatch custom event for dynamic components
        window.dispatchEvent(new CustomEvent('languageChanged', {
            detail: {
                language: lang,
                isTamil: lang === 'ta'
            }
        }));
    }

    // Expose globals
    window.translations = TRANSLATIONS;
    window.t = t;
    window.changeLanguage = changeLanguage;
    window.currentLanguage = currentLang;
    window.applyTranslations = applyTranslations;

    // Listen to Settings "Preferred Language" dropdown changes if farmer changes it in settings
    document.addEventListener('change', function (e) {
        if (e.target && e.target.id === 'settings-language') {
            const val = e.target.value;
            if (val === 'Tamil') {
                changeLanguage('ta');
            } else if (val === 'English') {
                changeLanguage('en');
            }
        }
    });

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            applyTranslations();
        });
    } else {
        applyTranslations();
    }
})();
