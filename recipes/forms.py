from django import forms
from .models import Recipe

class ResgisterRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'serving',
            'serving_unit',
            'preparation_steps',
            'cover',
            'category',
        ]