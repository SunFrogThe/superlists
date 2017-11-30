import uuid

from django.db import models
from django.contrib import auth

# Fix for
# ValueError: The following fields do not exist in this model or are m2m fields: last_login
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    def __str__(self):
        return self.email

class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4,
                           max_length=40)
