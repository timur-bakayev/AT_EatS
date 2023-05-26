from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserType(models.Model):
    establishment = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)


