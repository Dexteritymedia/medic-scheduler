# Generated by Django 4.2 on 2023-10-27 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date_accepted',
            field=models.DateTimeField(null=True),
        ),
    ]
