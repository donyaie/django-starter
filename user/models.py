from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, DeletableModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, **extra_fields):
        user = self.model(**extra_fields)
        password = extra_fields.get('password')
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(**extra_fields)

    def create_superuser(self, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**extra_fields)


# User model using django abstract base user class
class User(BaseModel, AbstractBaseUser, PermissionsMixin, DeletableModel,):

    username = models.CharField(_('User Name'), max_length=64,
                                unique=True)

    phone_number = models.CharField(_('Phone Number'), max_length=16,
                                    blank=True, null=True,)

    email = models.EmailField(_('Email'),  blank=True, null=True,)

    full_name = models.CharField(_('Full name'), max_length=128,
                                blank=True)

    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    is_guest = models.BooleanField(_('is_guest'), default=False)

    is_phone_number_verified = models.BooleanField(_('Is phone number verified'),
                                                default=False)
    is_email_verified = models.BooleanField(_('Is email verified'),
                                            default=False)
    avatar = models.ForeignKey('contents.Image', related_name='users',
                            on_delete=models.PROTECT, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Username and password are already required

    def avatar_tag(self):
        return mark_safe(
            '<img src="%s" style="box-shadow: rgba(87, 87, 87, 0.75) 6px 8px 9px 0px;border: 1px solid rgba(87, 87, 87, 0.75);border-radius: 3px;" width="150" height="150" />'
            % (self.avatar.content.url))

    avatar_tag.short_description = 'AvatarImage'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        name = ""
        if self.is_guest:
            name = "Guest"
        else:
            name = self.username

        return name

    @staticmethod
    def autocomplete_search_fields():
        return 'username',


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    
    is_notification_enabled = models.BooleanField(_('Is Notification Enabled'),default=True)
