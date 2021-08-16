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


# Commentsのデータを操作するマネージャークラスを新たに作成
class CommentsManager(models.Manager):

    def fetch_by_theme_id(self, theme_id):
        # 該当するtheme_idでフィルターして、idで昇順にソートして全件取得
        return self.filter(theme_id=theme_id).order_by('id').all()


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

    objects = CommentsManager()

    class Meta:
        db_table = 'comments'
