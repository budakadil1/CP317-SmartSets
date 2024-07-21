from django.forms import ModelForm, TextInput

from .models import Sets


class CreateDeckForm(ModelForm):
    class Meta:
        model = Sets
        fields = ["name", "description", "card_count", "author", "public"]
        exclude = ("author", "card_count", 'shared_with', 'slug',)

class EditDeck(ModelForm):
    class Meta:
        model = Sets
        fields = ["name", "description", "card_count", "author", "public"]
        exclude = ("author", "card_count", 'shared_with', 'slug',)