from django.contrib import admin
from .models import Post, Profile, Comment
from django.contrib import admin
from .models import Post, Profile, Comment, Tag

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Tag)
