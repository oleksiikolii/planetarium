# Generated by Django 4.2.4 on 2023-08-10 19:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("planetarium", "0005_astronomyshow_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ticket",
            options={"ordering": ["row", "seat"]},
        ),
    ]
