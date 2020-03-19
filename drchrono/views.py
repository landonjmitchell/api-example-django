import datetime

from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView, DetailView, FormView
from social_django.models import UserSocialAuth
from django.http import HttpResponseRedirect


import api_helpers
from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, PatientEndpoint
from .models import Doctor, Appointment, Patient
from .forms import StatusForm, CheckInForm, DemographicForm


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'kiosk_setup.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_requests(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've proved that the OAuth setup is working. Populate Doctor, Patient, and Appointment tables.
        """

        access_token = self.get_token()
        doctor_endpoint = DoctorEndpoint(access_token)
        api_helpers.populate_doctors(doctor_endpoint)
        doctor = Doctor.objects.first()

        self.request.session['doctor_id'] = doctor.id
        self.request.session['access_token'] = access_token

        # Populate patient and appointment tables with patients and appointments for the given doctor.

        patient_endpoint = PatientEndpoint(access_token)
        api_helpers.populate_patients(patient_endpoint, doctor)
        appointment_endpoint = AppointmentEndpoint(access_token)
        api_helpers.populate_appointments(appointment_endpoint, doctor)

        return doctor

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor = self.make_api_requests()

        context = {
            'doctor': doctor,
        }

        return context


class AppointmentsView(TemplateView):
    template_name = 'appointment/detail.html'

    # FIXME: simplify getting doctor and average wait time
    
    def get_context_data(self, **kwargs):
        context = super(AppointmentsView, self).get_context_data(**kwargs)

        access_token = self.request.session['access_token']
        doctor_id = self.request.session['doctor_id']

        doctor_endpoint = DoctorEndpoint(access_token)
        doctor = doctor_endpoint.fetch(doctor_id)

        appointment_endpoint = AppointmentEndpoint(access_token)
        wait_time = api_helpers.get_avg_wait_time(appointment_endpoint, doctor)
        context['avg_wait_time'] = wait_time
        context['doctor'] = doctor
        context['appointment'] = False

        return context

    
class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointment/detail.html'
    context_object_name = 'appointment'
    form_class = StatusForm

    # FIXME: simplify getting doctor and average wait time
    def get_context_data(self, **kwargs):
        context = super(AppointmentDetailView, self).get_context_data(**kwargs)

        access_token = self.request.session['access_token']
        doctor_id = self.request.session['doctor_id']
        doctor = Doctor.objects.get(pk=doctor_id)

        appointment_endpoint = AppointmentEndpoint(access_token)
        wait_time = api_helpers.get_avg_wait_time(appointment_endpoint, doctor)
        context['avg_wait_time'] = wait_time
        context['doctor'] = doctor

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        appointment_id = kwargs['pk']

        if form.is_valid():
            status = form.cleaned_data['status']
            access_token = self.request.session['access_token']

            appointment_endpoint = AppointmentEndpoint(access_token)
            response = appointment_endpoint.update(appointment_id, {'status': status})

            # FIXME: find a better way to update/refresh template view
            access_token = self.request.session['access_token']
            doctor_id = self.request.session['doctor_id']
            doctor = Doctor.objects.get(pk=doctor_id)
            api_helpers.populate_appointments(appointment_endpoint, doctor)

            # TODO: move logic to model methods?
            app = Appointment.objects.get(pk=appointment_id)
            if status == 'Checked In':
                app.check_in_time = datetime.datetime.now()
            elif status == 'In Session':
                app.start_time = datetime.datetime.now()
                if app.check_in_time:
                    app.wait_time = app.start_time - app.check_in_time
                else:
                    app.wait_time = 0
            elif status == 'Cancelled':
                app.wait_time = 0

        return HttpResponseRedirect(self.request.path_info)

        
class CheckInView(FormView):
    form_class = CheckInForm
    template_name = 'check_in/check_in.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            social_security_number = form.cleaned_data['social_security_number']

            patient = Patient.objects.first(first_name=first_name, last_name=last_name, social_security_number=social_security_number)

            if not patient:
                # TODO: display patient not found error
                pass
            else:
                date = datetime.datetime.today
                statuses = ['', None]
                appointment = Appointment.objects.first(patient=patient, scheduled_time__date=date, status__in=statuses)

                if not appointment:
                    # TODO: display no matching appointment error
                    pass
                else:
                    # TODO: display success, option to edit demographics or check_in
                    pass

# TODO: convert to class based view for consistency
def update_demographics(request, patient_id):
    p = get_object_or_404(Patient, pk=patient_id)
    if request.POST:
        form = DemographicForm(request.POST, instance=l)
        if form.is_valid():
            patient = form.save()
            return redirect('update_demographics', patient.id)

    else:
        form = DemographicForm(instance=p)

    return render(request, 'check_in/demographics.html', {'form': form})
