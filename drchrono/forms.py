from django import forms
from django.forms import widgets


class StatusForm(forms.Form):
    status = forms.CharField(max_length=25)

