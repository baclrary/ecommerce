from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = "authentication"

urlpatterns = [
    # path('', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('registration/', views.Registration.as_view(), name='registration_view'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh_view'),
]
