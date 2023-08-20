# Generated by Django 4.2.4 on 2023-08-09 13:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("planetarium", "0002_showsession_show_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("row", "seat", "show_session")},
        ),
    ]
