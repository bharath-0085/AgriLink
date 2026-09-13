"""
Agri Link — AI Module Views
=============================
APIs for Crop Recommendation, Plant Leaf Disease Detection, and Gemini Chatbot.
"""

import logging
import numpy as np
from PIL import Image
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from django.conf import settings
from apps.core.authentication import OptionalTokenAuthentication
from apps.core.exceptions import AIModelError, ExternalServiceError
from apps.core.utils import success_response, error_response
from apps.ai_module.model_loader import AIModelLoader
from apps.ai_module.serializers import CropRecommendSerializer, DiseaseDetectSerializer, ChatbotSerializer
from apps.ai_module.treatments import get_treatment_info

logger = logging.getLogger(__name__)


# ============================================================
# Crop Recommendation API
# ============================================================

# Fertilizer suggestions per crop
CROP_FERTILIZER_MAP = {
    "Rice": {"fertilizer": "Urea + DAP", "season": "Kharif (Jun–Nov)", "yield": "4–6 tonnes/ha"},
    "Maize": {"fertilizer": "NPK 10-26-26 + Urea", "season": "Kharif/Rabi", "yield": "5–7 tonnes/ha"},
    "Chickpea": {"fertilizer": "SSP + Rhizobium inoculant", "season": "Rabi (Oct–Mar)", "yield": "1–2 tonnes/ha"},
    "Kidney Beans": {"fertilizer": "SSP + Potash", "season": "Kharif", "yield": "1–1.5 tonnes/ha"},
    "Pigeon Peas": {"fertilizer": "Phosphate + Sulphur", "season": "Kharif", "yield": "1–2 tonnes/ha"},
    "Moth Beans": {"fertilizer": "Low NPK, drought tolerant", "season": "Kharif", "yield": "0.5–1 tonne/ha"},
    "Mung Bean": {"fertilizer": "SSP + Potash", "season": "Kharif/Summer", "yield": "1–1.5 tonnes/ha"},
    "Black Gram": {"fertilizer": "DAP at sowing", "season": "Kharif/Rabi", "yield": "1–1.5 tonnes/ha"},
    "Lentil": {"fertilizer": "SSP + low Nitrogen", "season": "Rabi (Oct–Feb)", "yield": "1–2 tonnes/ha"},
    "Pomegranate": {"fertilizer": "NPK 100:50:50 g/plant", "season": "Year-round", "yield": "15–20 kg/plant"},
    "Banana": {"fertilizer": "NPK 200:30:300 g/plant", "season": "Year-round (tropical)", "yield": "25–40 tonnes/ha"},
    "Mango": {"fertilizer": "NPK + Micronutrients", "season": "Summer (Apr–Jun)", "yield": "10–20 tonnes/ha"},
    "Grapes": {"fertilizer": "NPK 150:60:200 kg/ha", "season": "Mar–Jun", "yield": "15–25 tonnes/ha"},
    "Watermelon": {"fertilizer": "NPK 60:30:30 kg/ha", "season": "Summer/Kharif", "yield": "20–30 tonnes/ha"},
    "Muskmelon": {"fertilizer": "NPK 50:25:25 kg/ha", "season": "Summer", "yield": "15–20 tonnes/ha"},
    "Apple": {"fertilizer": "NPK + Boron", "season": "Summer (Oct–Nov harvest)", "yield": "15–20 tonnes/ha"},
    "Orange": {"fertilizer": "NPK + Lime", "season": "Winter (Nov–Jan)", "yield": "10–15 tonnes/ha"},
    "Papaya": {"fertilizer": "NPK 200:250:500 g/plant", "season": "Year-round", "yield": "40–50 tonnes/ha"},
    "Coconut": {"fertilizer": "NPK 1000:500:2000 g/palm", "season": "Year-round (coastal)", "yield": "70–100 nuts/tree"},
    "Cotton": {"fertilizer": "NPK 120:60:60 kg/ha", "season": "Kharif (Jun–Oct)", "yield": "2–3 tonnes/ha"},
    "Jute": {"fertilizer": "Urea + SSP + MOP", "season": "Kharif (Mar–Jun)", "yield": "2–3 tonnes/ha"},
    "Coffee": {"fertilizer": "NPK + organic manure", "season": "Biennial bearing", "yield": "1–2 tonnes/ha"},
}

def _get_crop_extras(crop_name):
    """Return fertilizer, season, yield for a given crop name."""
    info = CROP_FERTILIZER_MAP.get(crop_name, {})
    return {
        "fertilizer_suggestion": info.get("fertilizer", "Balanced NPK fertilizer recommended."),
        "suitable_season": info.get("season", "Varies by region and climate."),
        "expected_yield": info.get("yield", "Depends on soil and irrigation conditions."),
    }


class CropRecommendView(APIView):
    """
    POST /api/v1/ai/crop-recommend/

    Recommends optimal crops based on soil and weather parameters.
    Returns enriched response: crop name, confidence, season, fertilizer, yield hint.
    Accessible without authentication so farmers can use it from the dashboard.
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CropRecommendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        # Load model and optional scaler/encoder
        model, scaler, encoder, feature_names = AIModelLoader.get_crop_model()

        # Standard features: N, P, K, temperature, humidity, ph, rainfall
        input_data = [
            data["N"],
            data["P"],
            data["K"],
            data["temperature"],
            data["humidity"],
            data["ph"],
            data["rainfall"],
        ]

        try:
            features = np.array([input_data])

            if scaler:
                features = scaler.transform(features)

            prediction = model.predict(features)
            predicted_class = prediction[0]

            # Decode label
            if encoder:
                try:
                    crop_name = encoder.inverse_transform(prediction)[0]
                    crop_name = str(crop_name).strip().title()
                except Exception:
                    crop_name = str(predicted_class)
            else:
                # Use our crop label map or use prediction directly if it's a string
                label_map = AIModelLoader.get_crop_label_map()
                try:
                    # Try numeric index lookup (for models trained with integer labels)
                    crop_name = label_map.get(str(int(predicted_class)), str(predicted_class)).strip().title()
                except (ValueError, TypeError):
                    # Model already returns string class name directly (e.g. 'rice')
                    crop_name = str(predicted_class).strip().title()

            # Retrieve top 3 suggestions if predict_proba is supported
            suggestions = []
            confidence_pct = 0.0
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(features)[0]
                top_indices = np.argsort(probs)[::-1][:3]
                confidence_pct = round(float(probs[np.argmax(probs)]) * 100, 1)

                if encoder:
                    for idx in top_indices:
                        try:
                            c_name = encoder.classes_[idx]
                            suggestions.append({
                                "crop": str(c_name).strip().title(),
                                "probability": round(float(probs[idx]), 4),
                                "confidence_pct": round(float(probs[idx]) * 100, 1),
                            })
                        except Exception:
                            pass
                else:
                    label_map = AIModelLoader.get_crop_label_map()
                    model_classes = getattr(model, "classes_", None)
                    for idx in top_indices:
                        # Prefer model.classes_ (sklearn standard), then label_map, then index
                        if model_classes is not None and idx < len(model_classes):
                            c_name = str(model_classes[idx]).strip().title()
                        else:
                            try:
                                c_name = label_map.get(str(int(idx)), f"Crop {idx}").strip().title()
                            except (ValueError, TypeError):
                                c_name = f"Crop {idx}"
                        suggestions.append({
                            "crop": c_name,
                            "probability": round(float(probs[idx]), 4),
                            "confidence_pct": round(float(probs[idx]) * 100, 1),
                        })

            extras = _get_crop_extras(crop_name)

            # Save prediction record (if user is authenticated)
            try:
                from apps.ai_module.models import CropPrediction
                CropPrediction.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    nitrogen=data["N"],
                    phosphorus=data["P"],
                    potassium=data["K"],
                    temperature=data["temperature"],
                    humidity=data["humidity"],
                    ph=data["ph"],
                    rainfall=data["rainfall"],
                    recommended_crop=crop_name,
                    confidence=confidence_pct / 100.0,
                )
            except Exception as e:
                logger.warning("Could not save crop prediction record: %s", e)

            return success_response(
                data={
                    "recommended_crop": crop_name,
                    "confidence_pct": confidence_pct,
                    "top_suggestions": suggestions,
                    "fertilizer_suggestion": extras["fertilizer_suggestion"],
                    "suitable_season": extras["suitable_season"],
                    "expected_yield": extras["expected_yield"],
                    "reason": (
                        f"Based on N={data['N']}, P={data['P']}, K={data['K']}, "
                        f"pH={data['ph']}, Temp={data['temperature']}°C, "
                        f"Humidity={data['humidity']}%, Rainfall={data['rainfall']}mm - "
                        f"the AI model recommends {crop_name} for optimal yield."
                    ),
                },
                message="Crop recommendation generated successfully.",
            )

        except Exception as e:
            logger.error("Crop prediction computation failed: %s", e)
            raise AIModelError(f"Crop prediction failed: {e}")


# ============================================================
# Disease Detection API
# ============================================================

class DiseaseDetectView(APIView):
    """
    POST /api/v1/ai/disease-detect/

    Detects plant disease from an uploaded leaf image.
    Returns: Disease Name, Confidence, Treatment, and Prevention tips.
    Stores prediction history in DiseasePrediction model.
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DiseaseDetectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image_file = serializer.validated_data["image"]

        # Load Keras model and class names
        model, class_names = AIModelLoader.get_disease_model()

        try:
            image = Image.open(image_file).convert("RGB")

            try:
                target_height = model.input_shape[1]
                target_width = model.input_shape[2]
                if target_height is None or target_width is None:
                    target_height, target_width = 224, 224
            except Exception:
                target_height, target_width = 224, 224

            image = image.resize((target_width, target_height))
            img_array = np.array(image) / 255.0
            img_batch = np.expand_dims(img_array, axis=0)

            predictions = model.predict(img_batch)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])

            if class_names and class_idx < len(class_names):
                raw_class = class_names[class_idx]
            else:
                raw_class = f"Class {class_idx}"

            treatment_info = get_treatment_info(raw_class)

            # Upload image to Cloudinary for history
            image_url = ""
            try:
                from apps.core.utils import upload_to_cloudinary
                image_file.seek(0)
                image_url = upload_to_cloudinary(image_file, folder="agrilink/disease_scans")
            except Exception as e:
                logger.warning("Could not upload disease scan image to Cloudinary: %s", e)

            # Save prediction record
            try:
                from apps.ai_module.models import DiseasePrediction
                DiseasePrediction.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    image_url=image_url,
                    predicted_disease=treatment_info["disease_name"],
                    confidence=round(confidence, 4),
                )
            except Exception as e:
                logger.warning("Could not save disease prediction record: %s", e)

            return success_response(
                data={
                    "predicted_class": raw_class,
                    "disease_name": treatment_info["disease_name"],
                    "confidence": round(confidence, 4),
                    "confidence_pct": round(confidence * 100, 1),
                    "suggested_treatment": treatment_info["suggested_treatment"],
                    "prevention": treatment_info["prevention"],
                    "image_url": image_url,
                },
                message="Disease detection finished.",
            )

        except Exception as e:
            logger.error("Disease detection failed: %s", e)
            raise AIModelError(f"Disease detection failed: {e}")


# ============================================================
# Gemini Chatbot API
# ============================================================

class ChatbotView(APIView):
    """
    POST /api/v1/ai/chatbot/

    Handles queries with conversation history for context-aware responses.
    Accepts:
      - message: current user message (string)
      - history: list of {role: "user"|"bot", message: "..."} (optional)
    Stores history per authenticated user.
    """

    authentication_classes = [OptionalTokenAuthentication]
    permission_classes = [AllowAny]

    SYSTEM_INSTRUCTION = (
        "You are 'Agri Link Bot', a helpful agricultural expert chatbot for Indian farmers. "
        "Answer ONLY questions related to: agriculture, farming, crops, soil, crop diseases, "
        "organic farming, cultivation methods, fertilizers, pesticides, veterinary care, "
        "marketplace prices, government farmer schemes (PM-KISAN, PMFBY, Kisan Credit Card, etc.), "
        "weather advice, and nearby agri services. "
        "If the user asks about anything unrelated to these topics, respond politely and state that "
        "you can only answer agricultural questions. "
        "Keep answers clear, practical, actionable, and written in simple language. "
        "When possible, give specific advice for Indian farming conditions."
    )

    def post(self, request):
        serializer = ChatbotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_message = serializer.validated_data["message"]
        history = request.data.get("history", [])  # List of {role, message}

        api_key = settings.GEMINI_API_KEY
        if not api_key:
            logger.error("GEMINI_API_KEY is not configured in settings.")
            return error_response(
                "AI Assistant is temporarily unavailable.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)

            # Build conversation contents from history
            contents = []
            if isinstance(history, list):
                for turn in history:
                    role = turn.get("role", "user")
                    msg = turn.get("message", "")
                    if not msg:
                        continue
                    # Gemini uses "user" and "model" roles
                    gemini_role = "model" if role == "bot" else "user"
                    contents.append(
                        types.Content(
                            role=gemini_role,
                            parts=[types.Part(text=msg)],
                        )
                    )

            # Append current user message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=user_message)],
                )
            )

            config = types.GenerateContentConfig(
                system_instruction=self.SYSTEM_INSTRUCTION,
                temperature=0.3,
            )

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                    config=config,
                )
            except Exception:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=contents,
                    config=config,
                )

            response_text = getattr(response, "text", None) or "I'm sorry, I couldn't process your request at this time."

            # Save to chatbot history for authenticated users
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
                        message=response_text,
                    )
                except Exception as e:
                    logger.warning("Could not save chatbot history: %s", e)

            return success_response(
                data={"reply": response_text},
                message="Chatbot response generated.",
            )

        except ImportError:
            logger.error("google-genai SDK package is not installed.")
            return error_response(
                "AI Assistant is temporarily unavailable.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            err_str = str(e).lower()
            logger.error("Gemini API call failed: %s", e)
            # Handle quota exceeded and auth errors gracefully
            if "quota" in err_str or "429" in err_str or "resource_exhausted" in err_str:
                return error_response(
                    "AI Assistant is temporarily unavailable. (Quota exceeded)",
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            if "api_key" in err_str or "invalid" in err_str or "401" in err_str or "403" in err_str:
                return error_response(
                    "AI Assistant is temporarily unavailable.",
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
            return error_response(
                "AI Assistant is temporarily unavailable.",
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


# ============================================================
# Chatbot History API
# ============================================================

class ChatbotHistoryView(APIView):
    """
    GET /api/v1/ai/chat-history/   — Get user's chatbot history (last 50 turns)
    DELETE /api/v1/ai/chat-history/ — Clear user's chatbot history
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.ai_module.models import ChatbotHistory
        history = ChatbotHistory.objects.filter(user=request.user).order_by("timestamp")[:50]
        data = [
            {
                "role": h.role,
                "message": h.message,
                "timestamp": h.timestamp.isoformat(),
            }
            for h in history
        ]
        return success_response(data=data)

    def delete(self, request):
        from apps.ai_module.models import ChatbotHistory
        deleted_count, _ = ChatbotHistory.objects.filter(user=request.user).delete()
        return success_response(
            data={"deleted": deleted_count},
            message="Chat history cleared.",
        )
