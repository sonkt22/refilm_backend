from django.urls import path

from category.views import getCategories, createCategory, getCategory, updateCategory, deleteCategory

urlpatterns = [
    path('', getCategories, name='get_categories'),
    path('<str:categoryId>', getCategory, name='get_category'),
    path('create/', createCategory, name='create'),
    path('update/<str:categoryId>', updateCategory, name='update_category'),
    path('delete/<str:categoryId>', deleteCategory, name='delete_category'),
]