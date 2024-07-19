from django.db import models
from django.db.models import CharField, TextField, IntegerField, BooleanField, ForeignKey
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
# Create your models here.

class Sets(models.Model):
    name = CharField(blank=False, max_length=128)
    description = TextField()
    card_count = IntegerField()
    public = BooleanField() 
    shared_with = ForeignKey(User, on_delete=models.CASCADE, related_name="shared_with", blank=True, null=True)
    author = ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    slug = models.SlugField(default="", null=False)
    # will add decks here after

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.s = slugify(self.name)
        super(Sets, self).save(*args, **kwargs)

