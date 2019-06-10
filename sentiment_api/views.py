from sentiment_api.models import SentimentClass
from sentiment_api.serializers import SentimentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sentiment_api.sentiment import sentiment_analysis


class SentimentAnalysis(APIView):
    """
    Input the comments you want to do sentiment analysis.
    """

    def get(self, request, format=None):
        senti = SentimentClass.objects.all()
        serializer = SentimentSerializer(senti, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(request.data)
        list = sentiment_analysis(request.data["paragraph"])
        return Response(list, status=status.HTTP_200_OK)
