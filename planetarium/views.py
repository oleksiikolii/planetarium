from django.db.models import F, Count
from django_rest.permissions import IsAuthenticated
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from planetarium.models import ShowSession, Reservation, AstronomyShow, PlanetariumDome, ShowTheme
from planetarium.serializers import (
    ShowSessionSerializer,
    ReservationSerializer,
    AstronomyShowSerializer,
    ShowSessionRetrieveSerializer,
    PlanetariumDomeSerializer,
    ThemeSerializer,
    ShowImageSerializer,
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer,
)
from .permissions import IsAdminOrReadOnly


class ShowThemeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [IsAdminOrReadOnly]


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = [IsAdminOrReadOnly]


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = AstronomyShow.objects.prefetch_related(
        "themes"
    )
    serializer_class = AstronomyShowSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ShowImageSerializer

        if self.action == "list":
            return AstronomyShowListSerializer

        if self.action == "retrieve":
            return AstronomyShowRetrieveSerializer

        return AstronomyShowSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific show"""
        show = self.get_object()
        serializer = self.get_serializer(show, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowSessionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowSession.objects.select_related(
        "show"
    ).annotate(
        tickets_available=(
            F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row")
            - Count("tickets")
        )
    )
    serializer_class = ShowSessionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShowSessionRetrieveSerializer

        return ShowSessionSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title", None)
        themes_str = self.request.query_params.get("themes", None)

        queryset = self.queryset

        if title:
            queryset = queryset.filter(show__title__icontains=title)

        if themes_str:
            themes = [int(theme) for theme in themes_str.split(",")]
            queryset = queryset.filter(show__themes__id__in=themes)

        return queryset

    @extend_schema(
            parameters=[
                OpenApiParameter(
                    "title",
                    type=OpenApiTypes.STR,
                    description="Filter by show title (ex. ?title=fiction)",
                ),
                OpenApiParameter(
                    "themes",
                    type=OpenApiTypes.STR,
                    description="Filter by show title (ex. ?themes=1,2,3)",
                ),
            ]
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
