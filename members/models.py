from django.db import models
from django.contrib.auth.models import AbstractUser

from members.managers import MemberManager


SEX_CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)


class Member(AbstractUser):
    """Extended User model. Remove username and set email as the parameter for auth"""
    username = None
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MemberManager()

    name = models.CharField('Имя', max_length=50, db_index=True)
    surname = models.CharField('Фамилия', max_length=50, db_index=True)
    photo = models.ImageField('Фото', upload_to='members/photo')
    sex = models.CharField('Пол', max_length=6, choices=SEX_CHOICES)
    longitude = models.FloatField('Долгота')
    latitude = models.FloatField('Широта')
    liked_members = models.ManyToManyField('self', verbose_name='Симпатии', related_name='likes',
                                           blank=True, db_index=True)

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.email
