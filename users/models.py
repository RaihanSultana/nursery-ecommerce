from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save


# Create your models here.

class User(AbstractUser):
    admin = models.BooleanField(default=False)
    customer = models.BooleanField(default=False)

    username = models.CharField(max_length=255, unique=True)
    # email = models.EmailField(max_length=255, unique=True, null=True, blank=True)


class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Admin_profile')
    name = models.CharField(max_length=255)
    # admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Customer_profile')
    # name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='file_folder/', null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    # customer = models.BooleanField(default=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:  # What should the condition be here so that only the correct profile is created
        if instance.is_staff or instance.admin:
            AdminProfile.objects.get_or_create(user=instance)
        elif instance.customer:
            CustomerProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
