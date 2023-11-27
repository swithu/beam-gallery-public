from django.db import models
from account.models import CustomUser

# Create your models here.
class Category(models.Model):
    title = models.CharField(
        verbose_name='カテゴリ',
        max_length=20
    )

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(
        verbose_name='タグ',
        max_length=20
    )

    def __str__(self):
        return self.title


class PhotoPost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    )

    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )

    comment = models.TextField(
        verbose_name='コメント'
    )

    image1 = models.ImageField(
        verbose_name='イメージ１',
        upload_to = 'photos'
    )

    image2 = models.ImageField(
        verbose_name='イメージ２',
        upload_to='photos',
        blank=True,
        null=True
    )

    image3 = models.ImageField(
        verbose_name='イメージ３',
        upload_to='photos',
        blank=True,
        null=True
    )

    tag1 = models.ForeignKey(
        Tag,
        verbose_name='タグ1',
        on_delete=models.PROTECT,
        related_name='tag1_posts',
        blank=True,
        null=True
    )

    tag2 = models.ForeignKey(
        Tag,
        verbose_name='タグ2',
        on_delete=models.PROTECT,
        related_name='tag2_posts',
        blank=True,
        null=True
    )

    tag3 = models.ForeignKey(
        Tag,
        verbose_name='タグ3',
        on_delete=models.PROTECT,
        related_name='tag3_posts',
        blank=True,
        null=True
    )

    tag4 = models.ForeignKey(
        Tag,
        verbose_name='タグ4',
        on_delete=models.PROTECT,
        related_name='tag4_posts',
        blank=True,
        null=True
    )

    tag5 = models.ForeignKey(
        Tag,
        verbose_name='タグ5',
        on_delete=models.PROTECT,
        related_name='tag5_posts',
        blank=True,
        null=True
    )

    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    def __str__(self):
        return self.title