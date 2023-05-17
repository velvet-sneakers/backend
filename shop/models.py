from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from phone_field import PhoneField
import os


class ShopItems(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='shop', verbose_name='Фото товара')
    title = models.CharField(verbose_name='Название товара', max_length=255)
    desc = models.TextField(verbose_name='Описание товара')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id', 'title']


class Shoes(models.Model):
    name = models.CharField(verbose_name='Название обуви', max_length=255)
    image = models.ImageField(verbose_name='Изображение', upload_to='shoes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'


# Когда обувь будет удаляться, то и её фотография будет удалятся из media/shoes
@receiver(pre_delete, sender=Shoes)
def delete_image(sender, instance, **kwargs):
    image_path = instance.image.path

    if os.path.exists(image_path):
        os.remove(image_path)



'''
На случай может пригодиться
'''

# class UserManager(BaseUserManager):
#     def create_user(
#             self, email, phone, first_name, last_name, password):
#         """
#         Creates and saves a User with the given email, first name, last name, password and phone.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#         if not first_name:
#             raise ValueError('Users must have a first name')
#         if not last_name:
#             raise ValueError('Users must have a last name')
#         if not password:
#             raise ValueError('Users must have a password')
#         if not phone:
#             raise ValueError('Users must have a phone number')

#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             phone = phone
#         )

#         user.set_password(password)
#         return user

#     def create_superuser(self, email, phone, first_name, last_name, password):
#         """
#         Creates and saves a superuser with the given email, first name,
#         last name and password.
#         """
#         user = self.create_user(
#             email,
#             phone = phone,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name= 'E-mail', max_length=500, unique=True
    )
    phone = PhoneField(verbose_name='Номер телефона', max_length=20)
    # password по умолчанию в AbstractBaseUser
    # last_login по умолчанию в AbstractBaseUser
    first_name = models.CharField(verbose_name='Имя', max_length=50, blank=True)
    second_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
    address = models.CharField(verbose_name='Адрес', max_length=500, blank=True)

    is_staff = models.BooleanField(verbose_name='Employee status', default=False, help_text='Определяет, может ли пользователь пользоваться инфраструктурой Employee')
    # is_superuser по умолчанию в PermissionsMixin


    #Если будет нужно расскомментируйте эту строку
    # objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)