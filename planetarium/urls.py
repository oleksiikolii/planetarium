from django.urls import path, include

from rest_framework import routers

from planetarium.views import ShowSessionViewSet

router = routers.DefaultRouter()
router.register("show_sessions", ShowSessionViewSet, basename="sessions-list")


urlpatterns = router.urls

app_name = "planetarium"
