# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

def user_profile_picture_path(instance, filename):
    return f'profiles/user_{instance.id}/{filename}'

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        blank=True,
        null=True
    )
    # followers: users who follow THIS user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username
