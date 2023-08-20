from rest_framework import routers

from planetarium.views import (
    ShowSessionViewSet,
    ReservationViewSet,
    AstronomyShowViewSet,
)

router = routers.DefaultRouter()

router.register("show_sessions", ShowSessionViewSet, basename="sessions")
router.register("reservation", ReservationViewSet, basename="reservations")
router.register("shows", AstronomyShowViewSet, basename="shows")


urlpatterns = router.urls

app_name = "planetarium"
