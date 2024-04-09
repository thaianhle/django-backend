from django.urls import path
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
urlpatterns = [
    path("create/", views.create_product_type,name="create_product_type"),
    path("get/<str:product_id>/", views.get_product_by_id)
]