from django.db import models
from account_module.models import User

class ActiveUser(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    last_seen = models.DateTimeField(auto_now=True)
