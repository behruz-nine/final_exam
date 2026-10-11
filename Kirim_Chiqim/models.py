from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import AbstractUser
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
import random
from PROJECT.settings import EXPIRED_TIME_EMAIL, EXPIRED_TIME_PHONE
from datetime import datetime, timedelta


# Create your models here.
NEW, CODE_VERIFY, DONE = ('new', 'code verify', 'done')
VIA_EMAIL, VIA_PHONE = ('via email', 'via phone')

class Account(AbstractUser, BaseModel):
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE)
    )

    AUTH_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )

    phone_number = models.CharField(max_length=13, unique=True, null=True, blank= True)
    email = models.EmailField(max_length=20, unique=True, null=True, blank= True)
    auth_status = models.CharField(max_length=50, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=50, choices=AUTH_TYPE)
    


    def __str__(self):
        return self.username
    
    def default_username(self):
        if not self.username:
            u = str(uuid.uuid4())
            self.username = u[u.rfind('-'):]
            
            
            

    def default_password(self):
        if not self.password:
            u = str(uuid.uuid4())
            self.password = u[u.rfind('-'):]

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            password = self.password
            self.set_password(password)


    def email_normalize(self):
        email = self.email.lower()
        self.email = email

    
    def generate_code(self, verify_type):
        code = random.randint(1000, 9999)

        Verify.objects.create(
            verify_type = verify_type,
            code = code,
            user = self
        )
        return code


    def token(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token)
        }
    
    def save(self, *args, **kwargs):
        self.default_username()
        self.default_password()
        self.hashing_password()
        self.email_normalize()
        return super().save(*args, **kwargs)
    


class Verify(models.Model):
    VERIFY_TYPE = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE)
    )
    verify_type = models.CharField(max_length=20, choices=VERIFY_TYPE)
    code = models.CharField(max_length=4)
    expired_time = models.DateTimeField()
    used = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='codes')

    def __str__(self):
        return f"{self.user}----{self.code}"
    

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expired_time = datetime.now() + timedelta(minutes=EXPIRED_TIME_EMAIL)
        elif self.verify_type == VIA_PHONE:
            self.expired_time = datetime.now() + timedelta(minutes=EXPIRED_TIME_PHONE)
        return super().save(*args, **kwargs)