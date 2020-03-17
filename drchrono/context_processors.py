import datetime

from .models import Appointment

def todays_appointments(request):
    date = datetime.datetime.now()

    appointments = Appointment.objects.filter(
        scheduled_time__year=date.year,
        scheduled_time__month=date.month,
        scheduled_time__day=date.day,
    )
    return dict(todays_appointments=appointments)
