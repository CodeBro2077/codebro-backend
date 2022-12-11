from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(verbose_name='категория',
                            max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'


class Posts(models.Model):
    name = models.CharField(verbose_name='название поста',
                            max_length=30)

    created_by = models.ForeignKey(to=User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='post_creator')
    categories = models.ManyToManyField(Categories)
    markdown = models.TextField(verbose_name='разметка')
    description = models.TextField(verbose_name='описание')
    followers = models.ManyToManyField(User, related_name='post_followers')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'посты'
        verbose_name = 'пост'


class Images(models.Model):
    image = models.ImageField(verbose_name='фотография',
                              upload_to='posts_photos')

    class Meta:
        verbose_name_plural = 'фотографии'
        verbose_name = 'фотография'
