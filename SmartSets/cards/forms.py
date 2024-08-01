from django.forms import ModelForm, TextInput

from .models import Card


class CreateCardForm(ModelForm):
    class Meta:
        model = Card
        fields = ["question", "answer", "owner_set"]
