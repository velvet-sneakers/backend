from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
            self, email, phone, first_name, second_name, password):
        """
        Creates and saves a User with the given email, first name, last name, password and phone.
        """
        # if not email:
        #     raise ValueError('Users must have an email address')
        # if not first_name:
        #     raise ValueError('Users must have a first name')
        # if not second_name:
        #     raise ValueError('Users must have a second name')
        # if not password:
        #     raise ValueError('Users must have a password')
        # if not phone:
        #     raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            second_name=second_name,
            phone=phone
        )

        user.set_password(password)

        return user

    def create_superuser(self, email, first_name, second_name, password, phone):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
            first_name=first_name,
            second_name=second_name,
        )

        user.is_staff = True
        user.is_superuser = True

        return user
