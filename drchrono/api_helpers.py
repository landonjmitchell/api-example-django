import datetime

from .models import Doctor, Patient, Appointment

from endpoints import PatientEndpoint, AppointmentEndpoint

def populate_doctors(endpoint):
    """
    Populate Doctor table via API request.
    """
    for doctor_data in endpoint.list():
        data = {
            'first_name': doctor_data['first_name'],
            'last_name': doctor_data['last_name'],
            'npi_number': doctor_data['npi_number'],
            'profile_picture_url': doctor_data['profile_picture']
        }

        doctor, created = Doctor.objects.update_or_create(pk=doctor_data['id'], defaults=data)


def populate_patients(endpoint, doctor):
    """
    Populate Patient table with patients belonging to the given doctor.
    """
    patients = endpoint.list({'doctor': doctor.id})
    for patient_data in patients:
        data = {
            'doctor': doctor,
            'first_name': patient_data['first_name'],
            'last_name': patient_data['last_name'],
            'gender': patient_data['gender'],
            'date_of_birth': patient_data['date_of_birth'],
            'social_security_number': patient_data['social_security_number'],
            'address': patient_data['address'],
            'city': patient_data['city'],
            'state': patient_data['state'],
            'zip_code': patient_data['zip_code'],
            'email': patient_data['email'],
            'home_phone': patient_data['home_phone'],
            'cell_phone': patient_data['cell_phone']
        }

        patient, created = Patient.objects.update_or_create(pk=patient_data['id'], defaults=data)

def populate_appointments(endpoint, doctor):
        """
        Populate Appointment table with appointments belonging to the given doctor.
        """
        appointments = endpoint.list({'doctor': doctor.id, 'date': str(datetime.date.today())})
        for appointment_data in appointments:
            patient = Patient.objects.get(id=appointment_data['patient'])
            data = {
                'doctor': doctor,
                'patient': patient,
                'scheduled_time': appointment_data['scheduled_time'],
                'duration': appointment_data['duration'],
                'office': appointment_data['office'],
                'exam_room': appointment_data['exam_room'],
                'status': appointment_data['status']
            }

            appointment, created = Appointment.objects.update_or_create(
                defaults=data, pk=appointment_data['id'])
