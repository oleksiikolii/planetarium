from django.shortcuts import render
from rest_framework import viewsets

from planetarium.models import ShowSession
from planetarium.serializers import ShowSessionSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
