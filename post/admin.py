from django.contrib import admin

# Register your models here.
from .models import Post, UserCommentPost, UserLikePost

admin.site.register(Post)
admin.site.register(UserCommentPost)
admin.site.register(UserLikePost)

