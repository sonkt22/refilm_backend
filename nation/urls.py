from django.urls import path

from nation.views import getNations, createNation, getNation, updateNation, deleteNation

urlpatterns = [
    path('', getNations, name='get_nations'),
    path('<str:nationId>', getNation, name='get_nation'),
    path('create/', createNation, name='create'),
    path('update/<str:nationId>', updateNation, name='update_nation'),
    path('delete/<str:nationId>', deleteNation, name='delete_nation'),
]