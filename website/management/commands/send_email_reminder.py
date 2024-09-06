import datetime

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string, get_template
from django.core.mail import message, EmailMessage
from django.conf import settings

from website.models import Appointment

#To run the code enter python manage.py generate_promo_codes_and_prizes

class Command(BaseCommand):
    help = 'Send a reminder to patients whose appoinments are in two days time'

    def handle(self, *args, **kwargs):
        now = datetime.datetime.now()
        two_days_before = now + datetime.timedelta(days=2)
        print(two_days_before)
        

        #appointments = Appointment.objects.filter(date__gte=now, date__lte=two_days_before).all()
        #appointments = Appointment.objects.filter(date__gte=now, date__lte=two_days_before)
        appointments = Appointment.objects.filter(date=two_days_before).all()
        for appointment in appointments:
            print(appointment.first_name)
            print(appointment.time)
            print(appointment.request)
            data = {
                'fname': appointment.first_name,
                'date': appointment.date,
                'time': appointment.time,
            }
            #Added an email.html to the template folder
            message = get_template('email.html').render(data)
            print(message)
            """
            user = appointment.first_name
            time = appointment.time
            appointment.accepted = True
            data = {
                'fname': appointment.first_name,
                'date': appointment.date,
            }

        
            message = get_template('email.html').render(data)
            email = EmailMessage(
                "About your appointment",
                message,
                settings.EMAIL_HOST_USER,
                [appointment.email],
            )
            email.content_subtype = 'html'
            email.send()

            subject = ""
            message = f"Dear {user}"
            message += ""
            from_email = settings.EMAIL_HOST_USER
            recipient_email = [appointment.email]

            send_mail(subject, message, from_email, recipient_email)
            
            appointment.save()
            """
        
                     
            
