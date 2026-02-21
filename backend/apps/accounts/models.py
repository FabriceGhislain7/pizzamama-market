
import uuid
from django.contrib.auth.models import AbstractUser
from apps.core.models import TimeStampedModel
from django.db import models

# Create your models here.
class User(AbstractUser, TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marketing_consent = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username