from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.models import ContentType
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError('User mast have an username')
        if not password:
            raise ValueError('User mast have a password')
        username = self.model.normalize_username(username)
        user_object = self.model(username=username)
        user_object.set_password(password)
        user_object.admin = is_admin
        user_object.staff = is_staff
        user_object.active = is_active
        user_object.save(using=self._db)
        return user_object

    def create_stuffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(null=True, max_length=30)
    last_name = models.CharField(null=True, max_length=30)
    birthday = models.DateField(null=True)
    biography = models.TextField(null=True)
    contacts = models.CharField(null=True, max_length=150)
    password = models.CharField(max_length=240)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.username

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.username

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff


class RequestLog(models.Model):
    username = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField()
    path = models.TextField()
    method = models.CharField(max_length=7)
    status = models.IntegerField()
    execution_time = models.TimeField()

    def __str__(self):
        response = f'Username: {self.username}, Path: {self.path}'
        return response

class ChangeInModel(models.Model):
    app_label = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    action = models.CharField(max_length=100)

    def __str__(self):
        response = f'{self.app_label}.{self.model_name} entry was {self.action}'
        return response
