# Generated by Django 4.2.4 on 2023-08-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='showsession',
            name='show_time',
            field=models.DateTimeField(default='2000-01-01 20:00'),
            preserve_default=False,
        ),
    ]