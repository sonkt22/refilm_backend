import pytz
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Category
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser

# Create your views here.
from .serializers import CategorySerializer


@api_view(['GET'])
def getCategories(request):
    categories = Category.objects.filter(deleted_at=None)
    data = CategorySerializer(categories, many=True)
    return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)
    return JsonResponse(data=dict(data=categories), status=status.HTTP_200_OK)


@api_view(['GET'])
def getCategory(request, categoryId):
    try:
        category = Category.objects.get(id=categoryId, deleted_at=None)
        data = CategorySerializer(category, many=False)
        return JsonResponse(dict(data=data.data), status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return JsonResponse(dict(message='CATEGORY_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createCategory(request):
    category: dict = request.data
    if 'name' not in category.keys():
        return JsonResponse(data={'message': 'CATEGORY_NAME_REQUIRE'}, status=400)
    existCategory = Category.objects.filter(name=category['name'], deleted_at=None)
    if existCategory:
        return JsonResponse(data={'message': 'CATEGORY_EXISTED'}, status=409)
    newCategory = Category.objects.create(name=category['name'])
    newCategory.save()
    return JsonResponse(dict(id=newCategory.id, name=newCategory.name), status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateCategory(request, categoryId):
    category = Category.objects.filter(name=request.data['name'], deleted_at=None)
    arrCategory = list(category)
    if len(arrCategory) > 0 and str(categoryId) != str(arrCategory[0].id):
        return JsonResponse(data={'message': 'CATEGORY_EXISTED'}, status=409)
    try:
        category = Category.objects.get(id=categoryId, deleted_at=None)
    except Category.DoesNotExist:
        return JsonResponse(dict(message='CATEGORY_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    category.name = request.data['name']
    category.save()
    return JsonResponse(dict(id=categoryId, name=request.data['name']), status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteCategory(request, categoryId):
    try:
        category = Category.objects.get(id=categoryId, deleted_at=None)
    except Category.DoesNotExist:
        return JsonResponse(dict(message='CATEGORY_NOT_FOUND'), status=status.HTTP_404_NOT_FOUND)
    deletedAt = datetime.utcnow().replace(tzinfo=pytz.utc)
    category.deleted_at = deletedAt
    category.save()
    return JsonResponse(dict(status=True), status=status.HTTP_200_OK)