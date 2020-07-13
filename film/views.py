from datetime import datetime

import pytz
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.utils import json

from film.models import Film
from film.serializers import FilmSerializer


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createFilm(request):
    film: dict = request.POST
    if 'thumbnail' not in request.FILES:
        return JsonResponse(data={'message': 'FILM_THUMBNAIL_REQUIRE'}, status=400)
    if 'detail_picture' not in request.FILES:
        return JsonResponse(data={'message': 'FILM_DETAIL_PICTURE_REQUIRE'}, status=400)
    if 'name' not in film.keys():
        return JsonResponse(data={'message': 'FILM_NAME_REQUIRE'}, status=400)
    if 'title' not in film.keys():
        return JsonResponse(data={'message': 'FILM_TITLE_REQUIRE'}, status=400)
    if 'type' not in film.keys():
        return JsonResponse(data={'message': 'FILM_TYPE_REQUIRE'}, status=400)
    if 'producer_year' not in film.keys():
        return JsonResponse(data={'message': 'FILM_PRODUCER_YEAR_REQUIRE'}, status=400)
    if 'content' not in film.keys():
        return JsonResponse(data={'message': 'FILM_CONTENT_REQUIRE'}, status=400)
    if film['type'] != 'Movie' and film['type'] != 'Drama':
        return JsonResponse(data={'message': 'FILM_TYPE_MOVIE_OR_DRAMA'}, status=400)
    try:
        if int(film['producer_year']) > datetime.now().year:
            return JsonResponse(data={'message': 'FILM_PRODUCER_YEAR_FORMAT_YYYY'}, status=400)
    except ValueError:
        return JsonResponse(data={'message': 'FILM_PRODUCER_YEAR_FORMAT_YYYY'}, status=400)
    thumbnail = request.FILES['thumbnail']
    detailPicture = request.FILES['detail_picture']
    newFilm = Film.objects.create(
        name=film['name'],
        title=film['title'],
        producer_year=int(film['producer_year']),
        type=film['type'],
        content=film['content'],
        thumbnail=thumbnail,
        detail_picture=detailPicture,
    )
    newFilm.save()
    return JsonResponse(dict(id=newFilm.id,
                             name=newFilm.name,
                             title=newFilm.title,
                             type=newFilm.type,
                             producer_year=newFilm.producer_year,
                             content=newFilm.content,
                             thumbnail=json.dumps(str(newFilm.thumbnail)),
                             detail_picture=json.dumps(str(newFilm.detail_picture)),
                             review_point=newFilm.review_point,
                             review_count=newFilm.review_count,
                             ), status=status.HTTP_200_OK
                        )


@api_view(['GET'])
def getFilms(request):
    films = Film.objects.filter(deleted_at=None)
    data = FilmSerializer(films, many=True)
    return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)


@api_view(['GET'])
def getFilm(request, filmId):
    try:
        film = Film.objects.get(id=filmId, deleted_at=None)
        data = FilmSerializer(film, many=False)
        return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)
    except Film.DoesNotExist:
        return JsonResponse(dict(message='FILM_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateFilm(request, filmId):
    try:
        film = Film.objects.get(id=filmId, deleted_at=None)
    except Film.DoesNotExist:
        return JsonResponse(dict(message='FILM_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)

    if 'name' in request.data.keys():
        film.name = request.data['name']
    if 'title' in request.data.keys():
        film.title = request.data['title']
    if 'producerYear' in request.data.keys():
        film.producer_year = request.data['producerYear']
    if 'type' in request.data.keys():
        if request.data['type'] != 'Movie' and request.data['type'] != 'Drama':
            return JsonResponse(data={'message': 'FILM_TYPE_MOVIE_OR_DRAMA'}, status=400)
        film.type = request.data['type']
    if 'content' in request.data.keys():
        film.content = request.data['content']
    if 'thumbnail' in request.FILES.keys():
        film.thumbnail = request.FILES['thumbnail']
    if 'detailPicture' in request.FILES.keys():
        film.detail_picture = request.FILES['detailPicture']

    film.save()
    return JsonResponse(dict(id=film.id,
                             name=film.name,
                             title=film.title,
                             type=film.type,
                             producer_year=film.producer_year,
                             content=film.content,
                             thumbnail=json.dumps(str(film.thumbnail)),
                             detail_picture=json.dumps(str(film.detail_picture)),
                             review_point=film.review_point,
                             review_count=film.review_count,
                             ), status=status.HTTP_200_OK
                        )


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteFilm(request, filmId):
    try:
        film = Film.objects.get(id=filmId, deleted_at=None)
    except Film.DoesNotExist:
        return JsonResponse(dict(message='FILM_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    film.deleted_at = deletedAt
    film.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)
