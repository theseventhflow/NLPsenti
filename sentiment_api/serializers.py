from rest_framework import serializers
from sentiment_api.models import SentimentClass


class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentClass
        fields = ('id', 'title', 'code')