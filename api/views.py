from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # https://127.0.0.1:8000/api/movies/[movie ID]]/rate_movie
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        response = {'message': 'its working'}
        return Response(response, status=status.HTTP_200_OK)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

# Once views is up to date, need to update urls.py

