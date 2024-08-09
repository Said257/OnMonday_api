from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import timedelta


class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True)
    phone = models.CharField(max_length=40)
    # необязательные поля
    email = models.EmailField(max_length=100, blank=True, unique=True, null=True)
    photo = models.ImageField(upload_to='', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'мужчина'),
        ('female', 'женщина'),
        ('other', 'другой')
    ], blank=True, null=True)
    date_birth = models.DateField(blank=True, null=True)
    hobby = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)

    REQUIRED_FIELDS = ['phone', 'email', 'gender', 'hobby', 'country']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class UserEvents(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateTimeField()
    counter_users = models.IntegerField(default=2)

    users = models.ManyToManyField('User', related_name='participants')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятия'
        verbose_name_plural = 'Мероприятие'


