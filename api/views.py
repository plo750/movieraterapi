from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Limit access of users



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # Allow to pass token on POST request
    # And request.user is not more anymore: AnonymousUser
    authentication_classes = (TokenAuthentication,)
    # Limit the access of the movies, only if is authenticated
    # permission_classes = (AllowAny,) # Not loging needed
    permission_classes = (IsAuthenticated,)


    # http://127.0.0.1:8000/api/movies/[movie ID]/rate_movie/
    # in data => stars : '1-5'
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            # http://127.0.0.1:8000/api/movies/[pk value]]/rate_movie/
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user  # is part of the request ==> Not valid because no authentication has been done.
            # print('user: ', user)

            try:
                # user.id == ForeignKey also for the movie.id
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                # many = False ==> only one rating
                serializers = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializers.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                # We pass the all objects
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                # many = False ==>
                serializers = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializers.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide stars'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    # Limit the access of the movies, only if is authenticated
    permission_classes = (IsAuthenticated,)

    # Link in viewsets.ModelViewSet
    #   ==> mixins.UpdateModelMixin,
    #       ==> link in UpdateModelMixin and take the method

    # Prevent use the building default methods
    # Override existing one ===> Disable create from POST http://127.0.0.1:8000/api/ratings/
    def update(self, request, *args, **kwargs):
        response = {'message': 'you can update rating like this'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # Override existing one ===> Disable create from POST http://127.0.0.1:8000/api/ratings/
    def create(self, request, *args, **kwargs):
        response = {'message': 'you can create rating like this'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# Once views is up to date, need to update urls.py
