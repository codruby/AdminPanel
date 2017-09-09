from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class RabbitUserManager(BaseUserManager):
    """
    Application User Manager
    """

    def create_superuser(self, email, full_name, password):
        """
        Application User model
        """
        if not email:
            raise ValueError('User must have a valid username')

        user = self.model(
            email=email,
            full_name=full_name,
            is_admin=True)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, login_id, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not login_id:
            raise ValueError('The given login id must be set')
        # email = self.normalize_email(email)
        user = self.model(login_id=login_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login_id, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        return self._create_user(login_id, password, **extra_fields)


class RabbitUser(AbstractBaseUser):
    """
    Application User model
    """
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="name", default=None, max_length=100, unique=True)
    mobile = models.BigIntegerField(verbose_name="mobile", null=True)
    email = models.EmailField(verbose_name="email", unique=True)
    # login_id = models.IntegerField()
    login_id = models.CharField(verbose_name="login_id", unique=True, default=None, max_length=20, null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = RabbitUserManager()
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['name']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def get_short_name(self):
        '''
        Method for getting Name
        '''
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

    class Meta:
        '''model meta data'''
        verbose_name = "Rabbit User"
        verbose_name_plural = "Rabbit Users"
        db_table = "rabbituser"

    def __unicode__(self):
        '''model __unicode__ data'''
        return self.name


class HotelUser(models.Model):
    """
    Application User model
    """
    hotel_id = models.AutoField(primary_key=True)
    hotel_name = models.CharField(verbose_name="hotel_name", default=None, max_length=100, unique=True)
    contact_person = models.CharField(verbose_name="contact_person", default=None, max_length=50, null=True)
    contact_number = models.BigIntegerField(verbose_name="contact_number", null=True)
    contact_email = models.EmailField(verbose_name="contact_email", unique=True, null=True)
    hotel_address_line_1 = models.CharField(verbose_name="hotel_address_line_1", default=None, max_length=500, null=True)
    hotel_address_line_2 = models.CharField(verbose_name="hotel_address_line_2", default=None, max_length=500, null=True)
    hotel_address_line_3 = models.CharField(verbose_name="hotel_address_line_3", default=None, max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''model meta data'''
        verbose_name = "Application User"
        verbose_name_plural = "Application Users"
        db_table = "hoteluser"
        ordering = ['created_at']

    def __unicode__(self):
        '''model __unicode__ data'''
        return self.hotel_name


