from django.urls import path
from apps.ai_module import views

app_name = "ai_module"

urlpatterns = [
    path("crop-recommend/", views.CropRecommendView.as_view(), name="crop-recommend"),
    path("disease-detect/", views.DiseaseDetectView.as_view(), name="disease-detect"),
    path("chatbot/", views.ChatbotView.as_view(), name="chatbot"),
    path("chat-history/", views.ChatbotHistoryView.as_view(), name="chat-history"),
]
