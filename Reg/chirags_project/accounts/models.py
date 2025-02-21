from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, phone_no, location, dob, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_no=phone_no,
            location=location,
            dob=dob,
            is_active=True  # Ensure the user is active
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_no, location, dob, password):
        user = self.create_user(email, name, phone_no, location, dob, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    location = models.CharField(max_length=255)
    dob = models.DateField()
    login_time = models.DateTimeField(null=True, blank=True)  # Stores last login time
    token = models.CharField(max_length=100, null=True, blank=True)  # Stores auth token

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_no", "location", "dob"]

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"