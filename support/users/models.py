# Create your models here.
import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

User = settings.AUTH_USER_MODEL


class UserManager (BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise ValueError('The username must be set')
        if email is None:
            raise ValueError('The email must be set')
        try:
            user = self.model(username=username, email=email)
            user.set_password(password)
            user.save()
            user.save(using=self._db)
            return user
        except:
            raise

    def create_superuser(self, username, email, password):
        if password is None:
            raise ValueError('Superusers must have password')
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()


# custom user model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=30, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def _generate_jwt_token(self):
        exp_date = (datetime.now() + timedelta(days=10)).timestamp()
        token = jwt.encode({
            'id': self.pk,
            'exp': exp_date
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


# tickets model
class Comm(models.Model):
    comment = models.CharField(verbose_name='Enter comment', db_index=True, max_length=250)
    answer = models.CharField(verbose_name='Reply', blank=True, max_length=250)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    status_types = (
        ('in progress', 'In progress'),
        ('done', 'Done'),
        ('frozen', 'Frozen'),
    )
    status = models.CharField(verbose_name='Status', max_length=15, default='In progress', choices=status_types)
