from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import RegexValidator

# Create your models here.

class Profile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    bio = models.TextField(blank=True)
    date_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    egypt_phone_validator = RegexValidator(
    regex=r'^(?:\+20|0)?1[0125]\d{8}$',
    message="Enter a valid Egyptian phone number, e.g., +201012345678 or 01012345678."
    )
    
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[egypt_phone_validator]
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return  f"{self.username} - ({self.email})" 