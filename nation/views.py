import pytz
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import Nation
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser

# Create your views here.
from .serializers import NationSerializer


@api_view(['GET'])
def getNations(request):
    nations = Nation.objects.filter(deleted_at=None)
    data = NationSerializer(nations, many=True)
    return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)
    return JsonResponse(data=dict(data=categories), status=status.HTTP_200_OK)


@api_view(['GET'])
def getNation(request, nationId):
    try:
        nation = Nation.objects.get(id=nationId, deleted_at=None)
        data = NationSerializer(nation, many=False)
        return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)
    except Nation.DoesNotExist:
        return JsonResponse(dict(message='NATION_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createNation(request):
    nation: dict = request.data
    if 'name' not in nation.keys():
        return JsonResponse(data={'message': 'NATION_NAME_REQUIRE'}, status=status.HTTP_400_BAD_REQUEST)
    existNation = Nation.objects.filter(name=nation['name'], deleted_at=None)
    if existNation:
        return JsonResponse(data={'message': 'NATION_EXISTED'}, status=status.HTTP_409_CONFLICT)
    newNation = Nation.objects.create(name=nation['name'])
    newNation.save()
    return JsonResponse(dict(id=newNation.id, name=newNation.name), status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateNation(request, nationId):
    nation = Nation.objects.filter(name=request.data['name'], deleted_at=None)
    arrNation = list(nation)
    if len(arrNation) > 0 and str(nationId) != str(arrNation[0].id):
        return JsonResponse(data={'message': 'NATION_EXISTED'}, status=status.HTTP_409_CONFLICT)
    try:
        nation = Nation.objects.get(id=nationId, deleted_at=None)
    except Nation.DoesNotExist:
        return JsonResponse(dict(message='NATION_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    nation.name = request.data['name']
    nation.save()
    return JsonResponse(dict(id=nationId, name=request.data['name']), status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteNation(request, nationId):
    try:
        nation = Nation.objects.get(id=nationId, deleted_at=None)
    except Nation.DoesNotExist:
        return JsonResponse(dict(message='NATION_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    nation.deleted_at = deletedAt
    nation.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)
