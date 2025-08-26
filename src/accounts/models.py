import random
import string

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, first_name, last_name, email, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superadmin", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True.")
        if extra_fields.get("is_superadmin") is not True:
            raise ValueError("Superuser must have is_superadmin=True.")

        return self.create_user(first_name, last_name, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=50)
    last_name = models.CharField(_("last name"), max_length=50)
    username = models.CharField(_("username"), max_length=70, blank=True,null=True)
    email = models.EmailField(_("email"), max_length=254, unique=True)
    is_active = models.BooleanField(_("is active"), default=False)
    is_staff = models.BooleanField(_("is staff"), default=False)
    is_admin = models.BooleanField(_("is admin"), default=False)
    is_superadmin = models.BooleanField(_("is superadmin"), default=False)
    is_superuser = models.BooleanField(_("is superuser"), default=False)
    last_login = models.DateTimeField(_("last login"), auto_now_add=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    objects = CustomUserManager()
  


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
    
    def full_name(self):
        return f'{self.first_name}{self.last_name}'


    def generate_random_string(self, length=3):
        """Generate a random string of a given length."""
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=length))

    def save(self, *args, **kwargs):
        if not self.pk:
            # Only add the suffix for new objects
            base_username = f"{self.first_name}{self.last_name}"
            random_suffix = self.generate_random_string(3)
            # Create the final username with the random suffix
            self.username = f"{base_username}_{random_suffix}"
            # Ensure the generated username is unique
            while CustomUser.objects.filter(username=self.username).exists():
                random_suffix = self.generate_random_string(3)
                self.username = f"{base_username}_{random_suffix}"

        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures/", blank=True, null=True,default='users/default.png'
    )
    
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    pin_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email