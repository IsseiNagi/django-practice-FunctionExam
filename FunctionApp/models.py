from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
)

# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)  # Falseで登録がされ、メール認証でTrueになるイメージ
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
