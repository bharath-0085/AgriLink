from django.urls import path
from apps.marketplace import views

app_name = "marketplace"

urlpatterns = [
    # Product CRUD
    path("", views.ProductViewSet.as_view(), name="product-list"),
    path("bookmarks/", views.BookmarkView.as_view(), name="bookmark-list"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<str:order_id>/action/", views.OrderActionView.as_view(), name="order-action"),
    path("<str:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("<str:pk>/order/", views.OrderCreateView.as_view(), name="order-create"),

    # GPS nearby search
    path("nearby/", views.NearbyFarmersBuyersView.as_view(), name="nearby"),
]
