from django.urls import path
from .views import *

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('is_authenticated/', is_authenticated_view),
    path('is-username-taken/<username>/', is_username_taken_view),
    path('is-email-taken/<email>/', is_email_taken_view)


]
