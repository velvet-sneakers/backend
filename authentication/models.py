from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phone_field import PhoneField

from authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-mail', max_length=500, unique=True)
    phone = PhoneField(verbose_name='Номер телефона', max_length=20)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    second_name = models.CharField(verbose_name='Фамилия', max_length=150)
    address = models.CharField(verbose_name='Адрес', max_length=500, blank=True)
    is_staff = models.BooleanField(verbose_name='Employee status', default=False, help_text='Определяет, может ли пользователь пользоваться инфраструктурой Employee')
    # password по умолчанию в AbstractBaseUser
    # last_login по умолчанию в AbstractBaseUser
    # is_superuser по умолчанию в PermissionsMixin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        """
        Return the first_name plus the second_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.second_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)