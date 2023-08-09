from rest_framework import serializers

from planetarium.models import ShowSession


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = "__all__"
