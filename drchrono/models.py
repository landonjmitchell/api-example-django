import datetime

from django.db import models


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    npi_number = models.CharField(max_length=25)
    profile_picture_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
     return 'Doctor({}, {})'.format(self.first_name, self.last_name)


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True)
    social_security_number = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=2, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    home_phone = models.CharField(max_length=25, null=True)
    cell_phone = models.CharField(max_length=25, null=True)

    def __str__(self):
        return 'Patient({}, {})'.format(self.last_name, self.first_name)


class Appointment(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField()
    office = models.IntegerField()
    exam_room = models.IntegerField()
    status = models.CharField(max_length=20, null=True)
    check_in_time = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['scheduled_time']

    def check_in(self):
        self.check_in_time = datetime.datetime.now()

    def start(self):
        self.start_time = datetime.datetime.now()

    def __str__(self):
        if self.patient:
            return 'Appointment({} {} - {})'.format(self.patient.first_name, self.patient.last_name, self.scheduled_time)
        else:
            return 'Appointment(BREAK - {}'.format(self.scheduled_time)

