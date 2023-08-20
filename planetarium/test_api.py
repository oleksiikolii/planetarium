import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowSession, ShowTheme, PlanetariumDome
from planetarium.serializers import ShowSessionSerializer, ShowSessionRetrieveSerializer, AstronomyShowListSerializer, \
    AstronomyShowRetrieveSerializer

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def show_theme():
    return ShowTheme.objects.create(
        name="Jupiter"
    )


@pytest.fixture
def dome():
    return PlanetariumDome.objects.create(
        name="Blue",
        rows=20,
        seats_in_row=30
    )


@pytest.fixture
def show(show_theme):
    return AstronomyShow.objects.create(
        title="Jupiter Show",
        description="Some text",
    )


@pytest.fixture
def show_session(show, dome):
    session_data = {
        'show': show,
        'show_time': timezone.datetime(2022, 1, 1, 20, 0, tzinfo=timezone.utc),
        'planetarium_dome': dome,
    }
    return ShowSession.objects.create(**session_data)


@pytest.fixture
def superuser():
    User = get_user_model()
    return User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword'
    )


@pytest.fixture
def authenticated_superuser_client(superuser):
    client = APIClient()
    response = client.post(
        reverse("user:token_obtain_pair"),
        data={
            'email': 'admin@example.com',
            'password': 'adminpassword'
        },
        format='json'
    )
    assert response.status_code == 200
    token = response.json()['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def authenticated_client():
    client = APIClient()
    user_data = {
        "email": "test@test.com",
        "password": "testpassword",
    }
    client.post(reverse("user:create"), data=user_data)
    response = client.post(reverse("user:token_obtain_pair"), data=user_data)
    assert response.status_code == 200

    token = response.json()["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    return client


@pytest.mark.django_db
def test_list_show_sessions(authenticated_client, show_session):
    url = reverse("planetarium:sessions-list")
    response = authenticated_client.get(url)

    show_sessions = ShowSession.objects.all()
    data = ShowSessionSerializer(show_sessions, many=True).data
    data[0]["tickets_available"] = 600

    assert response.status_code == 200
    assert response.data == data


@pytest.mark.django_db
def test_detail_show_session(authenticated_client, show_session):
    serialized_session = ShowSessionRetrieveSerializer(show_session, many=False).data

    url = reverse(
        "planetarium:sessions-detail",
        args=[1]
    )
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data == serialized_session


@pytest.mark.django_db
def test_authorizing_show_session_post(
        authenticated_client,
        authenticated_superuser_client,
        show,
        dome
):
    user_post = authenticated_client.post(reverse("planetarium:sessions-list"))
    admin_post = authenticated_superuser_client.post(reverse("planetarium:sessions-list"))
    admin_post_with_data = authenticated_superuser_client.post(
        reverse("planetarium:sessions-list"),
        data={
            "show_time": "2023-07-15T18:00:00Z",
            "show": 1,
            "planetarium_dome": 1
        }
    )

    assert user_post.status_code == 403
    assert admin_post.status_code == 400
    assert admin_post_with_data.status_code == 201


@pytest.mark.django_db
def test_shows_list(authenticated_client, show):
    response = authenticated_client.get(reverse("planetarium:shows-list"))
    shows = AstronomyShow.objects.all()
    data = AstronomyShowListSerializer(shows, many=True).data

    assert response.status_code == 200
    assert response.data == data


@pytest.mark.django_db
def test_detail_show(authenticated_client, show):
    serialized_show = AstronomyShowRetrieveSerializer(show, many=False).data

    url = reverse(
        "planetarium:shows-detail",
        args=[1]
    )
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data == serialized_show


@pytest.mark.django_db
def test_authorizing_show_post(
        authenticated_client,
        authenticated_superuser_client,
        dome,
        show_theme
):
    user_post = authenticated_client.post(reverse("planetarium:shows-list"))
    admin_post = authenticated_superuser_client.post(reverse("planetarium:shows-list"))
    admin_post_with_data = authenticated_superuser_client.post(
        reverse("planetarium:shows-list"),
        data={
            "title": "Bronx",
            "description": "some text",
            "themes": [1],
        }
    )

    assert user_post.status_code == 403
    assert admin_post.status_code == 400
    assert admin_post_with_data.status_code == 201
