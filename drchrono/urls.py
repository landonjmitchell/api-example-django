from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin

from .models import Appointment
admin.autodiscover()

import views


urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='setup'),
    url(r'^welcome/$', views.DoctorWelcome.as_view(), name='setup'),
    url(r'^appointment/(?P<pk>[A-Za-z0-9]+)/$', 
        views.AppointmentDetailView.as_view(), 
        name='appointment_detail'),

    url(r'^appointment/$',
        views.AppointmentsView.as_view(), 
        name='appointments'),

    url(r'^kiosk/$', views.CheckInView.as_view(), name='check_in'),
    url('^demographics/(?P<patient_id>[\w-]+)/$',
        views.update_demographics, name='update_demographics'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
