from django.urls import path

from film.views import createFilm, getFilms, getFilm, updateFilm, deleteFilm

urlpatterns = [
    path('', getFilms, name='get_films'),
    path('<str:filmId>', getFilm, name='get_film'),
    path('create/', createFilm, name='create'),
    path('update/<str:filmId>', updateFilm, name='update_film'),
    path('delete/<str:filmId>', deleteFilm, name='delete_film'),
]