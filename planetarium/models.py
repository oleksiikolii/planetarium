import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


def show_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/shows/", filename)


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    themes = models.ManyToManyField(
        ShowTheme,
        related_name="shows"
    )
    image = models.ImageField(null=True, upload_to=show_image_file_path)

    def __str__(self):
        return self.title


class ShowSession(models.Model):
    show_time = models.DateTimeField()
    show = models.ForeignKey(
        AstronomyShow,
        on_delete=models.CASCADE,
        related_name="sessions"
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.show_time


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ["row", "seat", "show_session"]
