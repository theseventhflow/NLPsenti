from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from sentiment_api import views

urlpatterns = [
    path('sentiment/', views.SentimentAnalysis.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)