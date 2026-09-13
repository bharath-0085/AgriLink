"""
Agri Link — AI Model Loader
=============================
Lazy loads pre-trained AI models on-demand to speed up startup time.
Supports fallback to root-level model files if AI/ subdirectory files are missing.
"""

import json
import logging
import os
import joblib

from django.conf import settings
from apps.core.exceptions import AIModelError

logger = logging.getLogger(__name__)


class AIModelLoader:
    _crop_model = None
    _crop_scaler = None
    _crop_encoder = None
    _crop_feature_names = None
    _crop_label_map = None

    _disease_model = None
    _disease_classes = None

    @classmethod
    def get_crop_model(cls):
        """Retrieve the crop recommendation model instance (lazy loaded)."""
        if cls._crop_model is None:
            # Primary path: AI/crop_recommendation/
            primary_dir = settings.AI_CROP_RECOMMENDATION_DIR
            # Fallback path: project root (where crop_model.pkl may also exist)
            fallback_dir = settings.BASE_DIR

            model_path = os.path.join(primary_dir, "crop_model.pkl")
            if not os.path.exists(model_path):
                # Try root fallback
                model_path = os.path.join(fallback_dir, "crop_model.pkl")

            if not os.path.exists(model_path):
                logger.error("Crop recommendation model pkl not found in AI/crop_recommendation/ or project root.")
                raise AIModelError("Crop recommendation model is not installed/available.")

            try:
                cls._crop_model = joblib.load(model_path)
                logger.info("Crop recommendation model loaded from: %s", model_path)

                model_dir = os.path.dirname(model_path)

                # Try loading optional scaler
                scaler_path = os.path.join(model_dir, "scaler.pkl")
                if not os.path.exists(scaler_path):
                    scaler_path = os.path.join(primary_dir, "scaler.pkl")
                if os.path.exists(scaler_path):
                    cls._crop_scaler = joblib.load(scaler_path)
                    logger.info("Crop recommendation scaler loaded.")

                # Try loading optional label encoder
                encoder_path = os.path.join(model_dir, "label_encoder.pkl")
                if not os.path.exists(encoder_path):
                    encoder_path = os.path.join(primary_dir, "label_encoder.pkl")
                if os.path.exists(encoder_path):
                    cls._crop_encoder = joblib.load(encoder_path)
                    logger.info("Crop recommendation label encoder loaded.")

                # Try loading feature names
                features_path = os.path.join(primary_dir, "feature_names.json")
                if os.path.exists(features_path):
                    with open(features_path, "r") as f:
                        cls._crop_feature_names = json.load(f)
                    logger.info("Crop recommendation feature names loaded.")

                # Load crop label map (used when no encoder is available)
                label_map_path = os.path.join(primary_dir, "crop_label_map.json")
                if os.path.exists(label_map_path):
                    with open(label_map_path, "r") as f:
                        cls._crop_label_map = json.load(f)
                    logger.info("Crop label map loaded.")

            except Exception as e:
                logger.error("Error loading crop recommendation model: %s", e)
                raise AIModelError(f"Error initializing crop recommendation model: {e}")

        return cls._crop_model, cls._crop_scaler, cls._crop_encoder, cls._crop_feature_names

    @classmethod
    def get_crop_label_map(cls):
        """Return the integer-to-crop-name mapping dict."""
        if cls._crop_label_map is None:
            label_map_path = os.path.join(settings.AI_CROP_RECOMMENDATION_DIR, "crop_label_map.json")
            if os.path.exists(label_map_path):
                with open(label_map_path, "r") as f:
                    cls._crop_label_map = json.load(f)
        return cls._crop_label_map or {}

    @classmethod
    def get_disease_model(cls):
        """Retrieve the plant disease detection Keras model (lazy loaded)."""
        if cls._disease_model is None:
            # Primary path: AI/disease_detection/
            primary_dir = settings.AI_DISEASE_DETECTION_DIR
            # Fallback: project root
            fallback_dir = settings.BASE_DIR

            model_path = os.path.join(primary_dir, "best_model.keras")
            if not os.path.exists(model_path):
                model_path = os.path.join(fallback_dir, "best_model.keras")
            if not os.path.exists(model_path):
                model_path = os.path.join(fallback_dir, "plant_disease_model.keras")

            classes_path = os.path.join(primary_dir, "class_names.json")
            if not os.path.exists(classes_path):
                classes_path = os.path.join(fallback_dir, "class_names.json")

            if not os.path.exists(model_path):
                logger.error("Disease detection model not found in AI/disease_detection/ or project root.")
                raise AIModelError("Plant disease model is not installed/available.")

            try:
                # Lazy import TensorFlow so other tasks start instantly
                import tensorflow as tf
                # Prevent TF from utilizing all GPU memory if run locally
                gpus = tf.config.list_physical_devices("GPU")
                if gpus:
                    try:
                        for gpu in gpus:
                            tf.config.experimental.set_memory_growth(gpu, True)
                    except Exception:
                        pass

                cls._disease_model = tf.keras.models.load_model(model_path, compile=False)
                logger.info("Plant disease detection Keras model loaded from: %s", model_path)

                if os.path.exists(classes_path):
                    with open(classes_path, "r") as f:
                        cls._disease_classes = json.load(f)
                    logger.info("Disease class names loaded.")
                else:
                    logger.warning("Class names JSON file not found.")
                    cls._disease_classes = []

            except Exception as e:
                logger.error("Error loading disease detection model: %s", e)
                raise AIModelError(f"Error initializing plant disease detection model: {e}")

        return cls._disease_model, cls._disease_classes
