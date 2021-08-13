from django.db import models

# Create your models here.


class ThemesManager(models.Manager):

    def fetch_all_themes(self):
        return self.order_by('id').all()


class Themes(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        'FunctionApp.Users',
        on_delete=models.CASCADE,
    )

    objects = ThemesManager()

    class Meta:
        db_table = 'themes'


class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'FunctionApp.Users',
        on_delete=models.CASCADE
    )
    theme = models.ForeignKey(
        'Themes',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'comments'
