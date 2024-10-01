from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import *
from .serializers import MovieSerializer
from rest_framework.response import Response
from rest_framework import status

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
        Movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)