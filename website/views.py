import datetime

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.core.mail import message, EmailMessage
from django.utils import timezone
from django.db.models import Avg, Min, Max, Sum, Count

from .models import Appointment

# Create your views here.


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("fname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)


class AppointmentView(TemplateView):
    template_name = "appointment-page.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        time = ['10:00', '14:00', '16:00']
        time_str = [datetime.datetime.strptime(x, "%H:%M").time() for x in time]
        for day_time in time_str[-2:]:
            print(day_time)
        print(time_str[1])
        now = timezone.now()
        seven_days_later = now + datetime.timedelta(days=7)
        date_to_string = seven_days_later.strftime('%Y-%m-%d')
        date_to_datetime_date = datetime.datetime.strptime(date_to_string, '%Y-%m-%d').date()
        
        if Appointment.objects.count() == 0:
            appointment = Appointment.objects.create(
                first_name=fname,
                last_name=lname,
                email=email,
                phone=mobile,
                request=message,
                date_accepted=seven_days_later,
                date=date_to_datetime_date,
            )

            appointment.save()
            
        last_recorded_appointment_date = Appointment.objects.order_by('date').last()
        print(last_recorded_appointment_date.date)
        track_appointment = Appointment.objects.all().values('date').annotate(count=Count('date'))
        print(track_appointment)
        
        print(time_str[0])
        print(time_str[-1])
        print(time_str[1:2])
        time=[print(time) for time in time_str[-2:]]
        
        for data in track_appointment:
            print(data)
            if data['date'] == last_recorded_appointment_date.date and data['count'] == 3:
                print("Creating a new date")
                new_date_recorded = last_recorded_appointment_date.date + datetime.timedelta(days=1)
                print(f"Recorded: {new_date_recorded}")
                appointment = Appointment.objects.create(
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    phone=mobile,
                    request=message,
                    date_accepted=seven_days_later,
                    date=new_date_recorded,
                    time=time_str[0],
                )

                appointment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    f"Thanks {fname.title()} for making an appointment, your appointment is scheduled on {new_date_recorded:%A}, {new_date_recorded:%d} of {new_date_recorded:%b} {new_date_recorded:%Y}!"
                )
                
            if data['date'] == last_recorded_appointment_date.date and data['count'] <= 2:
                print("Adding to an existing date")
                appointment = Appointment.objects.create(
                        first_name=fname,
                        last_name=lname,
                        email=email,
                        phone=mobile,
                        request=message,
                        date_accepted=seven_days_later,
                        date=last_recorded_appointment_date.date,
                        time=time_str[-1],
                        #time=[time for time in time_str[-2:]],
                )

                appointment.save()
                messages.add_message(
                    request, messages.SUCCESS,
                    f"Thanks {fname.title()} for making an appointment, your appointment is scheduled on {last_recorded_appointment_date.date:%c}!"
                )
        context = {}
        return HttpResponseRedirect("/")
        #return render(request, 'appointment-scheduled.html', context)

class ManageAppointmentView(ListView):
    template_name = 'manage-appointments.html'
    model = Appointment
    context_object_name = 'appointments'
    login_required = True
    paginate_by = 3


    def post(self, request):
        date = request.POST.get('date')
        appointment_id = request.POST.get('appointment-id')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.date_accepted = datetime.datetime.now()
        appointment.save()

        data = {
            'fname': appointment.first_name,
            'date': date,
        }

        """
        message = get_template('email.html').render(data)
        email = EmailMessage(
            "About your appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email],
        )
        email.content_subtype = 'html'
        email.send()
        """

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        #return HttpResponseRedirect(request.PATH)
        return redirect('manage')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "title": "Manage Appointments",
        })
        return context
            
        
