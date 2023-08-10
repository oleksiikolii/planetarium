# Generated by Django 4.2.4 on 2023-08-10 10:44

from django.db import migrations, models
import planetarium.models


class Migration(migrations.Migration):

    dependencies = [
        ('planetarium', '0004_alter_ticket_reservation_alter_ticket_show_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='astronomyshow',
            name='image',
            field=models.ImageField(null=True, upload_to=planetarium.models.show_image_file_path),
        ),
    ]