from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
)

from django.db.models.signals import post_save
from django.dispatch import receiver

from uuid import uuid4
from datetime import datetime, timedelta

from django.contrib.auth.models import UserManager

# Create your models here.


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)  # Falseで登録がされ、メール認証でTrueになるイメージ
    is_staff = models.BooleanField(default=False)
    picture = models.FileField(null=True, upload_to='picture/',)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=datetime.now()
        ).first()
        user = user_activate_token.user
        user.is_active = True
        user.save()


class UserActivateTokens(models.Model):
    token = models.UUIDField(db_index=True)
    expired_at = models.DateTimeField()
    user = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
    )

    # Managerを指定する
    objects = UserActivateTokensManager()

    class Meta:
        db_table = 'user_active_tokens'


@receiver(post_save, sender=Users)
def publish_token(sender, instance, **kwargs):
    # Modelを継承したUserActivateTokensクラスのオブジェクトを生成してcreateメソッドを実行する
    user_activate_token = UserActivateTokens.objects.create(
        # 引数で受けたinstance：senderで指定したUsersクラスのインスタンス
        user=instance,
        token=str(uuid4()),
        expired_at=datetime.now() + timedelta(days=1)
    )
    # 登録されているメールアドレスに、URLを記載して送るイメージで。代用的に下記のようにしておく。
    print(f'http://127.0.01:8000/activate_user/{user_activate_token.token}')
