from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator


class NeighbourListForm(forms.Form):
    n = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    x = forms.FloatField()
    y = forms.FloatField()


class NeighbourCreateForm(forms.Form):
    name = forms.CharField(max_length=255)
    x = forms.FloatField()
    y = forms.FloatField()
