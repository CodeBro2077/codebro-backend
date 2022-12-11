from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostAPIView.as_view()),
    path('categories/', views.get_categories),
]
