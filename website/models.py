from django.db import models

# Create your models here.
class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    request = models.TextField()
    phone = models.CharField(max_length=50)
    date_sent = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(auto_now_add=False, null=True)
    date = models.DateField(auto_now_add=False, null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ['-date_sent']
    
