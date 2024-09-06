# Generated by Django 4.2 on 2023-10-26 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('request', models.TextField()),
                ('phone', models.CharField(max_length=50)),
                ('date_sent', models.DateField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
                ('date_accepted', models.DateTimeField()),
            ],
            options={
                'ordering': ['-date_sent'],
            },
        ),
    ]
