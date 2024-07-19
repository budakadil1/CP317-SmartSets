from django.forms import ModelForm, TextInput

from .models import Sets


class CreateDeckForm(ModelForm):
    class Meta:
        model = Sets
        fields = ["name", "description", "card_count", "author", "public", "shared_with"]
        exclude = ("author", "card_count")
        widgets = {
            'shared_with': TextInput(attrs={'placeholder':'Enter a username'})
        }