from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_img/', blank=True, null=True, default='default_img/default.png')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username