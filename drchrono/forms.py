from django import forms
from django.forms import widgets


class StatusForm(forms.Form):
    status = forms.CharField(max_length=25)

class CheckInForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    social_security_number = forms.CharField(max_length=30)
