from django.urls import path
from .views import TextSearchView, VoiceSearchView

urlpatterns = [
    path('text_search/', TextSearchView.as_view(), name='text_search'),
    path('voice_search/', VoiceSearchView.as_view(), name='voice_search'),
]
