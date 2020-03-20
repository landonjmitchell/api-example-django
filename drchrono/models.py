from django.db import models
from django.utils import timezone


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    npi_number = models.CharField(max_length=25)
    profile_picture_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
     return 'Doctor({}, {})'.format(self.first_name, self.last_name)


class Patient(models.Model):
    STATES = [(x, x) for x in \
            ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]]
              
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True)
    social_security_number = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, choices=STATES)
    zip_code = models.CharField(max_length=10, blank=True)
    email = models.EmailField(null=True, blank=True)
    home_phone = models.CharField(max_length=25, null=True, blank=True)
    cell_phone = models.CharField(max_length=25, null=True, blank=True)

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
    wait_time = models.IntegerField(null=True)

    def check_in(self):
        self.status = "Checked In"
        date = timezone.now()
        self.check_in_time = date

        self.save()

    def start(self):
        self.status = "In Session"
        date = timezone.now()
        self.start_time = date

        if self.check_in_time:
            self.wait_time = (self.start_time - self.check_in_time).total_seconds() // 60
        else:
            self.wait_time = 0

        self.save()

    def cancel(self):
        self.status = "Cancelled"
        self.wait_time = 0

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        if self.patient:
            return 'Appointment({} {} - {})'.format(self.patient.first_name, self.patient.last_name, self.scheduled_time)
        else:
            return 'Appointment(BREAK - {}'.format(self.scheduled_time)

