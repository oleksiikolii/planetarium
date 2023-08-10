from django.db import transaction
from rest_framework import serializers

from planetarium.models import ShowSession, Ticket, Reservation, AstronomyShow, ShowTheme, PlanetariumDome


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["row", "seat", "show_session"]


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ["tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
                return reservation


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = "__all__"


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "themes", "image"]


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    themes = ThemeSerializer(many=True)

    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "themes", "image"]


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ["name"]


class ShowSessionSerializer(serializers.ModelSerializer):
    tickets_available = serializers.IntegerField(read_only=True)
    show_title = serializers.CharField(
        source="show.title",
        read_only=True
    )
    planetarium_dome_name = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show",
            "show_title",
            "show_time",
            "planetarium_dome",
            "planetarium_dome_name",
            "tickets_available"
        )


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    show = AstronomyShowSerializer(many=False, read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(many=False, read_only=True)

    class Meta:
        model = ShowSession
        fields = ["id", "show", "show_time", "planetarium_dome"]


class ShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "image")
