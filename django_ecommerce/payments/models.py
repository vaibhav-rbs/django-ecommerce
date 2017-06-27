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

    @classmethod
    def create(cls, name, email, password, last_4_digits, stripe_id):
        new_user = cls(name=name, email=email, password=password,
                        stripe_id=stripe_id)
        new_user.set_password(password)
        new_user.save()
        return new_user
