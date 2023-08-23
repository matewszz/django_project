from typing import Any, Dict
from django import forms
from recipes.models import Recipe
from utils.django_forms import add_attr
from collections import defaultdict

from utils.strings import is_positive_number

class RegisterRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        
        self._my_errors = defaultdict(list) #Usando esse metado, o field pode receber todos os erros feitos no clean de uma vez


    class Meta:
        model = Recipe
        fields = 'title', 'serving_unit', 'preparation_time', \
            'preparation_time_unit', 'category', 'serving', 'description', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'serving_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                ),
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'span-2'
                }
            ),       
            }

    def clean(self):
        super_clean = super().clean()
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        if title is not None and description is not None and title == description:
            self.add_error('title', 'Cannot be equal to description')
            self.add_error('description', 'Cannot be equal to title')

        if title is not None and len(title) < 5:
            self.add_error('title', 'Title must have at least 5 chars.')

        return super_clean
    
    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)
        
        if not is_positive_number(field_value):
            self.add_error('preparation_time', 'Must be a positive number')

        return field_value
    
    def clean_serving(self):
        field_name = 'serving'
        field_value = self.cleaned_data.get(field_name)
        
        if not is_positive_number(field_value):
            self.add_error('serving', 'Must be a positive number')

        return field_value
    