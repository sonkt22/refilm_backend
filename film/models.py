from datetime import datetime
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django_enumfield import enum


class FilmType(enum.Enum):
    MOVIE = '0'
    DRAMA = '1'


class Film(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, null=True, blank=True)
    producer_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year)],
        help_text="Use the following format: <YYYY>", null=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='films/', blank=True, null=True)
    detail_picture = models.ImageField(upload_to='films/', blank=True, null=True)
    content = models.TextField(null=True, blank=True)
    review_point = models.FloatField(null=True, blank=True, default=0)
    review_count = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
