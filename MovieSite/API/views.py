from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import MovieSerializer, RegistrationSerializer, WatchlistSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movie = Movies.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail(request, pk):
    try:
        movie = Movies.objects.get(pk=pk)
    except Movies.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MovieSerializer(movie)  
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET','POST'])
def User_profile(request):

    if request.method == 'GET':
        return Response({"message": "please register to a new user."})
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




@api_view(['GET', 'POST'])
def Login_profile(request):
    if request.method == 'GET':
        return Response({'message': 'Please login to your account. '})
    
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful!',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def Logout_profile(request):
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as er:
        return Response({'error':str(er)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def Watchlist_profile(request):
    user = request.user
    try:
        watchlist = Watchlist.objects.get(user=user)
    except Watchlist.DoesNotExist:

        if request.method == 'POST':
            watchlist = Watchlist.objects.create(user=user)
        else:
            return Response({'error': 'watchlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = WatchlistSerializer(watchlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movit_to_watchlist(request):
    user = request.user
    movie_id = request.data.get('movie_id')

    if not movie_id:
        return Response({"error": "Movie ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        watchlist = Watchlist.objects.get(user=user)
        movie = Movies.objects.get(id=movie_id)
    except Watchlist.DoesNotExist:
        return Response({"error": "Watchlist not found"}, status=status.HTTP_404_NOT_FOUND)
    except Movies.DoesNotExist:
        return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

    if movie not in watchlist.movies.all():
        watchlist.movies.add(movie)
        return Response({"message": "Movie added to watchlist"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Movie already in watchlist"}, status=status.HTTP_200_OK)
