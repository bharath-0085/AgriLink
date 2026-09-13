"""
Agri Link — AI Assistant Dedicated API View
===========================================
Dedicated API endpoint for the AI Assistant chat module.
Handles POST /api/ai-assistant/chat/
Isolated from other modules.
"""

import logging
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from apps.core.authentication import OptionalTokenAuthentication

logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = (
    "You are 'Agri Link AI', an expert agricultural and agronomy assistant dedicated to Indian farmers. "
    "Your purpose is to provide expert farming advice, crop cultivation guidance, pest and disease solutions, "
    "soil health tips, irrigation methods, fertilizer/NPK dosage schedules, seasonal recommendations, seed varieties, "
    "and Indian government farmer schemes (such as PM-KISAN, PMFBY, Kisan Credit Card, Soil Health Card).\n\n"
    "Tone & Formatting Guidelines:\n"
    "- Provide clear, practical, structured, and actionable guidance for Indian agricultural conditions.\n"
    "- Organize answers using numbered sections or clear headings (e.g., '1. Growing Season & Climate', '2. Soil & Land Preparation', '3. Sowing & Spacing', '4. Fertilizer Schedule', '5. Disease & Pest Management').\n"
    "- Use bold labels for key parameters (e.g., **Best Soil:**, **Ideal Temp:**, **NPK Ratio:**, **Sowing Time:**).\n"
    "- Use clean nested bullet points for actionable steps and specific dosage.\n"
    "- Keep explanations accessible, supportive, and respectful to farmers."
)


def get_agri_expert_fallback(query: str, language: str = "en") -> str:
    """
    Intelligent Indian agronomy domain fallback when Gemini API key or network is unreachable.
    Provides structured sections, bold labels, and nested bullet points in English or Tamil.
    """
    is_tamil = str(language).strip().lower() in ["ta", "tamil"]
    q = query.lower()

    if any(k in q for k in ["paddy", "rice"]):
        if is_tamil:
            return (
                "### 1. பயிர் பருவம் & காலநிலை\n"
                "* **கார்/குறுவை பருவம்:** ஜூன்–ஜூலை விதைப்பு, அக்டோபர்–நவம்பர் அறுவடை.\n"
                "* **சம்பா/தாளடி பருவம்:** ஆகஸ்ட்–செப்டம்பர் விதைப்பு, ஜனவரி–பிப்ரவரி அறுவடை.\n"
                "* **உகந்த வெப்பநிலை:** 22°C முதல் 32°C வரை, போதுமான சூரிய ஒளி மற்றும் மிதமான ஈரப்பதம்.\n\n"
                "### 2. நிலம் தயாரித்தல் & மண் மேலாண்மை\n"
                "* **பொருத்தமான மண்:** களிமண் அல்லது வண்டல் கலந்த களிமண் (pH 5.5 - 7.0).\n"
                "* **சேற்றுழவு:** 2-3 முறை நன்கு சேறாக்கி சமன்படுத்தி நீர்க்கசிவைத் தடுக்கவும்.\n\n"
                "### 3. பரிந்துரைக்கப்பட்ட நெல் ரகங்கள் (தமிழ்நாடு)\n"
                "* **அதிக விளைச்சல் ரகங்கள்:** CO-51, ADT-45, BPT-5204 (சம்பா மசூரி), CR-1009 Sub-1.\n"
                "* **பாரம்பரிய/சிறப்பு ரகங்கள்:** சீரக சம்பா, தூயமல்லி, கருப்பு கவுனி.\n"
                "* **விதை அளவு:** நேரடி விதைப்புக்கு 15-20 கிலோ/ஏக்கர்; நாற்று நடவுக்கு 10-12 கிலோ/ஏக்கர்.\n\n"
                "### 4. உர மேலாண்மை & NPK அட்டவணை (ஏக்கருக்கு)\n"
                "* **அடி உரம்:** 50 கிலோ DAP + 25 கிலோ பொட்டாஷ் + 10 கிலோ துத்தநாக சல்பேட் (கடைசி உழவில்).\n"
                "* **முதல் மேலுரம் (20–25 நாள்):** 35 கிலோ யூரியா + 10 கிலோ வேப்பம்பிண்ணாக்கு.\n"
                "* **இரண்டாம் மேலுரம் (40–45 நாள் - தூர்க்கட்டும் பருவம்):** 35 கிலோ யூரியா + 15 கிலோ பொட்டாஷ்.\n\n"
                "### 5. நீர் மற்றும் பூச்சி மேலாண்மை\n"
                "* **நீர்ப்பாசனம்:** கதிர் வரும் வரை 2-3 செ.மீ நீர் தேங்க வைக்கவும்; அறுவடைக்கு 10 நாட்களுக்கு முன் நீரை வடிக்கவும்.\n"
                "* **குருத்துப்பூச்சி / இலைச்சுருட்டுப் புழு:** குளோரான்ட்ரனிலிப்ரோல் 18.5% SC @ 60 மி.லி/ஏக்கர் தெளிக்கவும்."
            )
        return (
            "### 1. Growing Season & Climate\n"
            "* **Kharif Season:** Sowing in June–July, harvesting in November–December.\n"
            "* **Rabi Season (Boro):** Sowing in November–December in irrigated belts.\n"
            "* **Ideal Temperature:** 22°C to 32°C with high humidity and abundant sunlight.\n\n"
            "### 2. Soil & Land Preparation\n"
            "* **Best Soil:** Clayey or clay loam with high water retention and pH 5.5 to 7.0.\n"
            "* **Puddling:** 2–3 wet plowings followed by leveling to prevent percolation losses.\n\n"
            "### 3. Recommended Seed Varieties (India)\n"
            "* **High Yielding:** IR-64, MTU-1010, BPT-5204 (Samba Mahsuri), Swarna (MTU-7029).\n"
            "* **Basmati:** Pusa Basmati 1121, Pusa Basmati 1509.\n"
            "* **Seed Rate:** 20–25 kg/acre for nursery transplanting.\n\n"
            "### 4. Fertilizer & NPK Schedule (Per Acre)\n"
            "* **Basal Dose:** 50 kg DAP + 25 kg MOP + 10 kg Zinc Sulphate (21%) at final puddling.\n"
            "* **First Top Dressing (20–25 DAT):** 35 kg Urea.\n"
            "* **Second Top Dressing (40–45 DAT - Panicle Initiation):** 35 kg Urea + 15 kg MOP.\n\n"
            "### 5. Water & Pest Management\n"
            "* **Water Regime:** Maintain 2–3 cm water depth during early vegetative phase; drain before harvest.\n"
            "* **Stem Borer / Leaf Folder:** Spray Chlorantraniliprole 18.5% SC @ 60 ml/acre or Cartap Hydrochloride 50% SP @ 400 g/acre."
        )

    if any(k in q for k in ["tomato", "blight", "curl"]):
        if is_tamil:
            return (
                "### 1. நோய் கண்டறிதல் & அறிகுறிகள்\n"
                "* **முன் பருவ இலைக்கருகல் (Early Blight):** கீழ் இலைகளில் வளைய வடிவிலான பழுப்பு நிறப் புள்ளிகள்.\n"
                "* **பின் பருவ இலைக்கருகல் (Late Blight):** இலைகளில் ஈரமான கறுப்பு நிறத் திட்டுகளும் வெள்ளை நிறப் பூஞ்சையும்.\n"
                "* **இலைச்சுருட்டு வைரஸ் நோய்:** வெள்ளை ஈக்களால் பரவும் இலை சுருங்குதல் மற்றும் வளர்ச்சி குன்றுதல்.\n\n"
                "### 2. உடனடி சிகிச்சை & தெளிக்கும் அட்டவணை\n"
                "* **பூஞ்சைக் கருகல் கட்டுப்பாடு:**\n"
                "  * *தடுப்பு முறை:* மேன்கோசெப் 75% WP @ 2.5 கிராம்/லிட்டர் தண்ணீர்.\n"
                "  * *குணப்படுத்தும் முறை:* மெட்டலாக்ஸில் 8% + மேன்கோசெப் 64% WP @ 2 கிராம்/லிட்டர் அல்லது அஸோக்சிஸ்ட்ரோபின் 23% SC @ 1 மி.லி/லிட்டர்.\n"
                "* **வெள்ளை ஈ கட்டுப்பாடு (இலைச்சுருட்டுக்கு):**\n"
                "  * ஏக்கருக்கு 15–20 மஞ்சள் வண்ண ஒட்டும் பொறிகளை அமைக்கவும்.\n"
                "  * அசிடமிப்ரிட் 20% SP @ 0.5 கிராம்/லிட்டர் அல்லது வேப்பெண்ணெய் கரைசல் 3% தெளிக்கவும்.\n\n"
                "### 3. தடுப்பு நடவடிக்கைகள்\n"
                "* பாதிக்கப்பட்ட கீழ் இலைகளை உடனே அகற்றி அழிக்கவும்.\n"
                "* இலைகள் மீது நீர் தேங்காமல் சொட்டுநீர்ப் பாசனத்தைப் பயன்படுத்தவும்."
            )
        return (
            "### 1. Diagnosis & Symptoms\n"
            "* **Early Blight (Alternaria solani):** Target-like concentric brown rings on older lower leaves.\n"
            "* **Late Blight (Phytophthora infestans):** Water-soaked blackish patches with white mildew underneath in humid cool weather.\n"
            "* **Tomato Leaf Curl Virus:** Upward curling, stunted plant growth, transmitted by whiteflies.\n\n"
            "### 2. Immediate Treatment & Spray Schedule\n"
            "* **Fungal Blight Control:**\n"
            "  * *Preventive:* Mancozeb 75% WP @ 2.5 g/L water.\n"
            "  * *Curative:* Metalaxyl 8% + Mancozeb 64% WP @ 2 g/L or Azoxystrobin 23% SC @ 1 ml/L water.\n"
            "* **Whitefly / Vector Control (For Leaf Curl):**\n"
            "  * Install yellow sticky traps (15–20 traps/acre).\n"
            "  * Spray Acetamiprid 20% SP @ 0.5 g/L or Diafenthiuron 50% WP @ 1.2 g/L water.\n\n"
            "### 3. Preventive Agronomic Measures\n"
            "* Remove and burn severely infected bottom foliage to prevent spore splash.\n"
            "* Avoid overhead sprinkler irrigation; prefer drip lines to keep leaf canopies dry.\n"
            "* Practice crop rotation with non-solanaceous crops (maize, pulses, or cereals)."
        )

    if any(k in q for k in ["pm-kisan", "pm kisan", "scheme", "subsidy", "installment", "kcc"]):
        if is_tamil:
            return (
                "### 1. பிஎம்-கிசான் (PM-KISAN) திட்ட விவரம்\n"
                "* **பயன்:** தகுதியான விவசாயக் குடும்பங்களுக்கு ஆண்டுக்கு ₹6,000, 4 மாதங்களுக்கு ஒருமுறை ₹2,000 வீதம் 3 தவணைகளாக வங்கி கணக்கில் நேரடியாக (DBT) செலுத்தப்படுகிறது.\n"
                "* **நிர்வாகம்:** மத்திய வேளாண்மை மற்றும் விவசாயிகள் நல அமைச்சகம்.\n\n"
                "### 2. அவசியமான தகுதிகள் & நிபந்தனைகள்\n"
                "* **ஆதார் இணைக்கப்பட்ட வங்கிக் கணக்கு:** வங்கி கணக்கு NPCI ஆதார் மேப்பிங் செய்யப்பட்டிருக்க வேண்டும்.\n"
                "* **நில உரிமை சரிபார்ப்பு:** பட்டா மற்றும் நில ஆவணங்கள் விவசாயி பெயரில் போர்ட்டலில் பதிவு செய்யப்பட வேண்டும்.\n"
                "* **e-KYC நிறைவு:** PM-KISAN போர்டல், Face Auth மொபைல் செயலி அல்லது CSC மையம் மூலம் முடிக்கப்பட வேண்டும்.\n\n"
                "### 3. தகுதி நிலையை அறிவது எப்படி?\n"
                "* அதிகாரப்பூர்வ இணையதளம்: `pmkisan.gov.in`\n"
                "* **'Know Your Status'** பகுதியில் ஆதார் எண் அல்லது பதிவு எண்ணை உள்ளிடவும்."
            )
        return (
            "### 1. PM-KISAN Scheme Overview\n"
            "* **Benefit:** ₹6,000 per eligible farmer family per year, released in 3 equal installments of ₹2,000 every 4 months directly via DBT.\n"
            "* **Administering Ministry:** Ministry of Agriculture & Farmers Welfare, Govt. of India.\n\n"
            "### 2. Mandatory Eligibility Prerequisites\n"
            "* **Aadhaar-Seeded Bank Account:** Bank account must be linked with active NPCI Aadhaar mapper.\n"
            "* **Land Record Seeding (Bhoomi Satyapan):** State revenue portal must verify land ownership in applicant's name.\n"
            "* **e-KYC Completion:** Mandatory via OTP on PM-KISAN portal, PM-KISAN mobile app (Face Auth), or nearest CSC center.\n\n"
            "### 3. How to Check Status\n"
            "* Visit official portal: `pmkisan.gov.in`\n"
            "* Tap on **'Know Your Status'** and input Registration Number or Aadhaar.\n"
            "* Verify three green checkmarks: *Land Seeding (Yes)*, *e-KYC Done (Yes)*, *Aadhaar Bank Account Seeded (Yes)*."
        )

    if any(k in q for k in ["cotton", "bollworm"]):
        if is_tamil:
            return (
                "### 1. பருத்தி சாகுபடி வழிமுறைகள்\n"
                "* **விதைப்பு பருவம்:** மே–ஜூன் (முன் பருவ மழையை ஒட்டி).\n"
                "* **இடைவெளி:** 90 செ.மீ × 60 செ.மீ அல்லது 120 செ.மீ × 45 செ.மீ.\n"
                "* **மண் வகை:** நல்ல வடிகால் வசதியுள்ள கரிசல் மண் (Regur soil).\n\n"
                "### 2. உர மேலாண்மை (ஏக்கருக்கு)\n"
                "* **அடி உரம்:** 50 கிலோ DAP + 30 கிலோ பொட்டாஷ் + 10 கிலோ சல்பர்.\n"
                "* **மேலுரம்:** யூரியா 30 கிலோ (30-வது நாளில்), 30 கிலோ (60-வது நாளில்).\n\n"
                "### 3. பூச்சி மேலாண்மை (இளஞ்சிவப்பு காய்ப்புழு)\n"
                "* ஏக்கருக்கு 5 பெரேமோன் பொறிகளை வைக்கவும்.\n"
                "* புரோபெனோபாஸ் 50% EC @ 2 மி.லி/லிட்டர் அல்லது இமேக்டின் பென்சோகேட் 5% SG தெளிக்கவும்."
            )
        return (
            "### 1. Cotton Cultivation Essentials\n"
            "* **Sowing Season:** May–June with onset of pre-monsoon showers.\n"
            "* **Spacing:** 90 cm × 60 cm or 120 cm × 45 cm for Bt Cotton hybrids.\n"
            "* **Soil:** Deep black clay soil (Regur) with good drainage.\n\n"
            "### 2. Fertilizer Management (Per Acre)\n"
            "* **Basal:** 50 kg DAP + 30 kg Potash + 10 kg Sulphur.\n"
            "* **Top Dressing:** Split Urea (30 kg at 30 DAS, 30 kg at 60 DAS squaring stage).\n\n"
            "### 3. Pest Management (Pink Bollworm & Sucking Pests)\n"
            "* Install pheromone traps @ 5 traps/acre for monitoring pink bollworm moths.\n"
            "* Spray Profenofos 50% EC @ 2 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L during flowering."
        )

    if any(k in q for k in ["fertilizer", "npk", "urea", "dap", "soil"]):
        if is_tamil:
            return (
                "### 1. NPK உரங்களின் பயன்கள்\n"
                "* **தழைச்சத்து - N (யூரியா 46% N):** பயிரின் செழிப்பான வளர்ச்சி மற்றும் தூர் கட்டுவதற்கு உதவுகிறது.\n"
                "* **மணிச்சத்து - P (DAP 18:46:0 அல்லது SSP 16% P):** வேர் ஆழமாகப் பாயவும் ஆரம்பக்கால பயிர் உறுதிக்கும் தேவை.\n"
                "* **சாம்பல் சத்து - K (பொட்டாஷ் 60% K2O):** நோய் எதிர்ப்பு சக்தி, திரட்சியான தானியங்கள் மற்றும் வறட்சியைத் தாங்க உதவுகிறது.\n\n"
                "### 2. மண் பயன்பாட்டு நெறிமுறைகள்\n"
                "* மண் பரிசோதனை அட்டை (Soil Health Card) பரிந்துரைப்படி உரம் இடவும்.\n"
                "* மணிச்சத்து மற்றும் சாம்பல் சத்தை அடி உரமாக உழவில் இடவும்; தழைச்சத்தை பிரித்து மேலுரமாக இடவும்."
            )
        return (
            "### 1. Understanding NPK Functions\n"
            "* **Nitrogen (N):** Promotes lush green vegetative canopy and tillering (Urea - 46% N).\n"
            "* **Phosphorus (P):** Stimulates deep root proliferation and early plant establishment (DAP - 18:46:0 or SSP - 16% P).\n"
            "* **Potassium (K):** Enhances disease resistance, grain filling, drought tolerance, and fruit weight (MOP - 60% K2O).\n\n"
            "### 2. General Soil Application Best Practices\n"
            "* Always base application on a **Soil Health Card (SHC)** report.\n"
            "* Apply all Phosphorus and Potash as **basal dose** during final tillage.\n"
            "* Split Nitrogen into 2–3 applications to prevent leaching losses in rainfed or flood-irrigated soils.\n"
            "* Incorporate 4–5 tonnes of well-decomposed FYM or compost per acre to enhance organic carbon."
        )

    # General expert agriculture fallback
    if is_tamil:
        return (
            "### 1. வேளாண் ஆலோசனை சுருக்கம்\n"
            f"* **தலைப்பு:** \"{query.strip()}\" குறித்த வழிகாட்டுதல்\n"
            "* **ஆலோசனை வகை:** இந்திய மற்றும் தமிழ்நாட்டு விவசாய நிலைமைகளுக்கான நிபுணர் பரிந்துரை.\n\n"
            "### 2. முக்கிய பரிந்துரைகள்\n"
            "* **கள மதிப்பீடு:** உரம் அல்லது மருந்து தெளிக்கும் முன் மண்ணின் ஈரப்பதம் மற்றும் தட்பவெப்பநிலையைச் சோதிக்கவும்.\n"
            "* **ஒருங்கிணைந்த பயிர் பாதுகாப்பு:** இயற்கை பூச்சி விரட்டிகள் மற்றும் பரிந்துரைக்கப்பட்ட சமச்சீர் உரங்களை இணைத்துப் பயன்படுத்தவும்.\n\n"
            "### 3. இன்றைய செயல் திட்டம்\n"
            "* தெளிப்புப் பணிகளுக்கு முன் உள்ளூர் வானிலை முன்னறிவிப்பைச் சரிபார்க்கவும்.\n"
            "* மேலும் விரிவான வழிகாட்டுதலுக்கு அக்ரி லிங்க் உதவி மையத்தை அல்லது உங்கள் வட்டார வேளாண்மை அலுவலரை அணுகவும்."
        )

    return (
        "### 1. Agronomy Consultation Summary\n"
        f"* **Topic:** Guidance regarding \"{query.strip()}\"\n"
        "* **Advisory Status:** Agricultural Expert Recommendations for Indian field conditions.\n\n"
        "### 2. Key Recommendations\n"
        "* **Field Assessment:** Inspect soil moisture, drainage conditions, and ambient temperature before applying field inputs.\n"
        "* **Integrated Management:** Combine organic soil conditioners (neem cake, FYM) with recommended balanced NPK doses.\n"
        "* **Preventive Protection:** Monitor pests using yellow/blue sticky traps and pheromone lures before resorting to chemical controls.\n\n"
        "### 3. Action Steps for Today\n"
        "* Verify local weather alerts and rainfall forecasts before scheduling spraying or fertilizer broadcasting.\n"
        "* Consult your local Krishi Vigyan Kendra (KVK) or Agri Link advisory channel for customized block-level schedules."
    )


class AIAssistantChatAPIView(APIView):
    """
    Dedicated AI Assistant Chat Endpoint for Agri Link.
    POST /api/ai-assistant/chat
    Accepts:
      {
        "message": "User query",
        "language": "en" | "ta",
        "conversationHistory": [
          {"role": "user"|"assistant", "text": "...", "timestamp": "..."}
        ]
      }
    Returns:
      {
        "success": true,
        "reply": "AI answer formatted in rich markdown",
        "conversationHistory": [...]
      }
    """
    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data or {}
        user_message = data.get("message") or data.get("prompt", "")
        if not user_message or not str(user_message).strip():
            return Response(
                {"success": False, "error": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_message = str(user_message).strip()
        raw_history = data.get("conversationHistory") or data.get("history", [])
        requested_language = str(data.get("language") or "").strip().lower()

        # Normalize incoming history
        normalized_history = []
        if isinstance(raw_history, list):
            for turn in raw_history:
                if not isinstance(turn, dict):
                    continue
                role = turn.get("role", "user")
                # Accept text or message
                text = turn.get("text") or turn.get("message", "")
                if text:
                    normalized_history.append({
                        "role": "assistant" if role in ["bot", "assistant", "model"] else "user",
                        "text": str(text).strip()
                    })

        reply_text = None

        # Attempt Gemini API if configured
        api_key = getattr(settings, "GEMINI_API_KEY", None)
        if api_key:
            try:
                from google import genai
                from google.genai import types

                client = genai.Client(api_key=api_key)

                contents = []
                # Keep last 6 context turns
                for turn in normalized_history[-6:]:
                    gemini_role = "model" if turn["role"] == "assistant" else "user"
                    contents.append(
                        types.Content(
                            role=gemini_role,
                            parts=[types.Part(text=turn["text"])],
                        )
                    )

                # Append current user message
                contents.append(
                    types.Content(
                        role="user",
                        parts=[types.Part(text=user_message)],
                    )
                )

                active_instruction = SYSTEM_INSTRUCTION
                if requested_language in ["ta", "tamil"]:
                    active_instruction += (
                        "\n\nCRITICAL LANGUAGE REQUIREMENT: The farmer has requested answers in Tamil (தமிழ்). "
                        "Formulate your entire response in clear, fluent, natural Tamil language using standard Tamil agricultural terms."
                    )

                config = types.GenerateContentConfig(
                    system_instruction=active_instruction,
                    temperature=0.3,
                )

                # Try preferred models
                response = None
                for model_candidate in ["gemini-3.5-flash", "gemini-3.6-flash"]:
                    try:
                        response = client.models.generate_content(
                            model=model_candidate,
                            contents=contents,
                            config=config,
                        )
                        if response and getattr(response, "text", None):
                            reply_text = response.text
                            break
                    except Exception as me:
                        logger.debug("Model %s failed: %s", model_candidate, me)
                        continue

            except Exception as e:
                logger.warning("Gemini API call failed, using agronomy fallback: %s", e)

        # If Gemini didn't return text, use expert Indian agronomy knowledge fallback
        if not reply_text:
            reply_text = get_agri_expert_fallback(user_message, language=requested_language)

        # Store in ChatbotHistory if authenticated
        if request.user and request.user.is_authenticated:
            try:
                from apps.ai_module.models import ChatbotHistory
                ChatbotHistory.objects.create(
                    user=request.user,
                    role=ChatbotHistory.ROLE_USER,
                    message=user_message,
                )
                ChatbotHistory.objects.create(
                    user=request.user,
                    role=ChatbotHistory.ROLE_BOT,
                    message=reply_text,
                )
            except Exception as db_err:
                logger.warning("Failed to persist ChatbotHistory: %s", db_err)

        # Build updated history
        updated_history = list(normalized_history)
        updated_history.append({"role": "user", "text": user_message})
        updated_history.append({"role": "assistant", "text": reply_text})

        return Response({
            "success": True,
            "reply": reply_text,
            "conversationHistory": updated_history,
            "data": {
                "reply": reply_text,
            }
        }, status=status.HTTP_200_OK)
