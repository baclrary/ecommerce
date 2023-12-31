from .views import *
from django.urls import path

app_name = "users"


urlpatterns = [
    path('profile/', UserProfile.as_view(), name='profile'),
    path('profile/settings/', UserInfo.as_view(), name='profile-settings'),
    path('profile/orders/', UserOrdersListView.as_view(), name='profile-orders'),
]