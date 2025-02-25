from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

class CustomerManager(BaseUserManager):
    def create_user(self, customer_name, customer_phone, customer_email, password=None):
        if not customer_email:
            raise ValueError("Customers must have an email address")
        email = self.normalize_email(customer_email)
        user = self.model(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, customer_name, customer_phone, customer_email, password):
        user = self.create_user(customer_name, customer_phone, customer_email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    customer_id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, unique=True)
    customer_email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    last_logged_in = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'customer_email'
    REQUIRED_FIELDS = ['customer_name', 'customer_phone']

    objects = CustomerManager()

    def __str__(self):
        return self.customer_name

    @property
    def id(self):
        return self.customer_id

    def generate_token(self):
        refresh = RefreshToken.for_user(self)
        self.token = str(refresh.access_token)
        self.save(update_fields=["token"])
        return self.token
