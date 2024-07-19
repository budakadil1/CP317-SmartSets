from django.db import models
from django.db.models import TextField, IntegerField, BooleanField, ImageField, ForeignKey
from sets.models import Sets
# Create your models here.
class Card(models.Model):
    question = TextField()
    answer = TextField()
    owner_set = ForeignKey(Sets, on_delete=models.CASCADE)