from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='slug')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name='posts')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[settings.PAGE_SIZE]
