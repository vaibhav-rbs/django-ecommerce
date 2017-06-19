from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models. CharField(max_length=255, unique=True)
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateField(auto_now=True)

    USETNAME_FIELD = 'email'

    def __str__(self):
        return self.email
