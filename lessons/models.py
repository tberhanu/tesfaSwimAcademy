from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(models.Model):
    email = models.EmailField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Store hashed password
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class UserRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.name} ({self.email})"
