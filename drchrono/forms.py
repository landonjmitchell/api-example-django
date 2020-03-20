from django import forms
from django.forms import widgets
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Patient, Appointment


from .models import Patient

class StatusForm(forms.Form):
    status = forms.CharField(max_length=25)

class CheckInForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    social_security_number = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(CheckInForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        social_security_number = cleaned_data.get('social_security_number')

        # verify patient exists
        patient = Patient.objects.filter(
                first_name=first_name,
                last_name=last_name,
                social_security_number=social_security_number
            ).first()
        if not patient: 
            raise ValidationError('No patient found matching this information')

        # verify appointment for patient today that has not already
        # been checked in to
        statuses = ['', None]
        date = timezone.now().date()
        appointment = Appointment.objects.filter(
            patient=patient, 
            scheduled_time__date=date, 
            status__in=statuses).first()
        if not appointment:
            raise ValidationError('No new appointments found for this patient today')

        return cleaned_data

 
    

class DemographicForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = ['id', 'doctor', 'first_name', 'last_name', 'gender', 'date_of_birth', 'social_security_number']


