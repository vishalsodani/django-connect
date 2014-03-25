from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from django_connect import tools
from django_connect.models import AbstractModel

from .choices import Genders


class UserManager(BaseUserManager):
    
    def create_user(self, username, password=None, **extra_fields):
        # Check for username
        if not username:
            raise ValueError('Username is a required field.')
        if not User.is_unique_username(username):
            raise ValueError('Username must be unique.')
        # Get user model instance
        user = self.model(username=username, **extra_fields)
        # Set user active
        user.is_active = True
        # Set hashed password
        user.set_password(password)
        # Save user
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        # Create user
        user = self.create_user(username, password, **extra_fields)
        # Set user staff
        user.is_staff = True
        # Set user active
        user.is_active = True
        # Set user superuser
        user.is_superuser = True
        # Save user
        user.save(using=self._db)
        return user

    def get_by_username_email_or_phone(self, username_email_or_phone):
        try:
            return User.objects.filter(
                Q(username__iexact=username_email_or_phone) | 
                Q(email__email__iexact=username_email_or_phone) | 
                Q(phone__phone=username_email_or_phone)
            ).get()
        except User.DoesNotExist:
            return None


class User(AbstractBaseUser, PermissionsMixin):
    PASSWORD_MIN_LENGTH = 8
    LANGUAGE_MIN_LENGTH = 2 

    NAME_MAX_LENGTH = 30
    USERNAME_MAX_LENGTH = 30
    LANGUAGE_MAX_LENGTH = 5
    TIMEZONE_MAX_LENGTH = 32

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)

    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)

    first_name = models.CharField(max_length=NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=NAME_MAX_LENGTH)

    birthday = models.DateField(blank=True, null=True)
    gender = models.IntegerField(blank=True, null=True, choices=Genders.CHOICES)

    language = models.CharField(choices=settings.LANGUAGES, max_length=LANGUAGE_MAX_LENGTH)
    timezone = models.CharField(max_length=TIMEZONE_MAX_LENGTH)

    is_seller = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('first_name', 'last_name',) # required for superuser creation

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def is_unique_username(username):
        return User.objects.filter(username__iexact=username).count() == 0

    @staticmethod
    def is_unique_email(email):
        return Email.objects.filter(email__iexact=email).count() == 0 and NewEmail.objects.filter(email__iexact=email).count() == 0

    @staticmethod
    def is_unique_phone(phone):
        return Phone.objects.filter(phone=phone).count() == 0 and NewPhone.objects.filter(phone=phone).count() == 0

    @staticmethod
    def prepare_birthday(birthday):
        month, day, year = birthday.split('/')
        return "{0}-{1}-{2}".format(year, month, day)


class EmailManager(models.Manager):
    def create_email(self, user, email, delete_new_email=True):
        # Get email model instance
        _email = self.model(user=user, email=UserManager.normalize_email(email))
        # Save email
        _email.save(using=self._db)
        if delete_new_email:
            # Delete new email
            NewEmail.objects.filter(email=email).delete()
        return _email


class Email(AbstractModel):
    EMAIL_MAX_LENGTH = 255

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='email')
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)

    objects = EmailManager()

    def __unicode__(self):
        return "%(user)s's email is %(email)s" % {
            'user':self.user.get_full_name(), 
            'email': self.email,
        }


class NewEmailManager(models.Manager):
    def create_new_email(self, user, email):
        # Get new_email model instance
        new_email = self.model(user=user, email=email)
        # Set key
        new_email.key = NewEmail.generate_key(email)
        # Save new_email
        new_email.save(using=self._db)
        return new_email


class NewEmail(AbstractModel):
    KEY_MAX_LENGTH = 32

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='new_email')
    email = models.EmailField(max_length=Email.EMAIL_MAX_LENGTH, unique=True)
    key = models.CharField(max_length=KEY_MAX_LENGTH)

    objects = NewEmailManager()

    def __unicode__(self):
        return "%(user)s's new email is %(email)s with key %(key)s" % {
            'user':self.user.get_full_name(), 
            'email': self.email,
            'key': self.key,
        }

    @staticmethod
    def generate_key(email):
        return tools.generate_key(length=NewEmail.KEY_MAX_LENGTH, extra=email)


# class PhoneManager(models.Manager):
#     def create_phone(self, user, phone, delete_new_phone=True):
#         # Get phone model instance
#         _phone = self.model(user=user, phone=phone)
#         # Save phone
#         _phone.save(using=self._db)
#         if delete_new_phone:
#             # Delete new phone
#             NewPhone.objects.filter(phone=phone).delete()
#         return _phone


# class Phone(AbstractModel):
#     PHONE_MAX_LENGTH = 20

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='phone')
#     phone = models.EmailField(max_length=PHONE_MAX_LENGTH, unique=True)

#     objects = PhoneManager()

#     def __unicode__(self):
#         return "%(user)s's phone is %(phone)s" % {
#             'user':self.user.get_full_name(), 
#             'phone': self.phone,
#         }


# class NewPhoneManager(models.Manager):
#     def create_new_phone(self, user, phone):
#         # Get new_phone model instance
#         new_phone = self.model(user=user, phone=phone)
#         # Set key
#         new_phone.key = NewPhone.generate_key()
#         # Save new_phone
#         new_phone.save(using=self._db)
#         return new_phone      


# class NewPhone(AbstractModel):
#     KEY_MAX_LENGTH = 8

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='new_phone')
#     phone = models.CharField(max_length=Phone.PHONE_MAX_LENGTH, unique=True)
#     key = models.CharField(max_length=KEY_MAX_LENGTH)

#     objects = NewPhoneManager()

#     def __unicode__(self):
#         return "%(user)s's new phone is %(phone)s with key %(key)s" % {
#             'user':self.user.get_full_name(), 
#             'phone': self.phone,
#             'key': self.key,
#         }

#     @staticmethod
#     def generate_key():
#         return tools.generate_digit_key(NewPhone.KEY_MAX_LENGTH)