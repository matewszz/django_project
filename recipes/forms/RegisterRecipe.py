from django import forms
from utils.django_forms import add_placeholder
from recipes.models import Recipe


class RegisterRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'serving', 'serving_unit', \
            'preparation_steps', 'cover'
