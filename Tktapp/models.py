import uuid
from distutils.command.upload import upload
from django.db import models
from .usermanager import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    full_name = models.CharField(max_length=25, blank='true')
    phone_no = models.IntegerField(null=True, blank=True, unique=True)
    is_author = models.BooleanField(default=False)
    # notice the absence of a "Password field", that is built in.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        return full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


user = get_user_model()


class Event(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    user = models.ForeignKey(user, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(blank=True, upload_to='images/')
    about = models.TextField()
    location = models.CharField(max_length=100)
    pin_location = models.CharField(max_length=255, blank=True)
    ticket_size = models.IntegerField()
    tickets_left = models.IntegerField(null=True,blank=True)
    start_date = models.DateField(auto_now_add=False, null=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    end_date = models.DateField(null=True, blank=True)
    has_categories = models.BooleanField(default=False)
    value = models.IntegerField(null=True,blank=True)
    
    def has_categories(self):
        if self.has_categories is False:
            return self.price
        else:
            return self.has_categories
    

    def __str__(self):
        return self.title


class Categories(models.Model):
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    category_name = models.CharField(max_length=25)
    value = models.IntegerField()


class Ticket(models.Model):
    User = models.ForeignKey(user, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=30 ,null=True ,blank=True)
    price = models.IntegerField()
    serial_no = models.CharField(max_length=20)
    ticket_type = models.CharField(max_length=20)
    saved = models.BooleanField(default=False, blank=True ,null=True)

