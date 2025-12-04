import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_admin_login(client, admin_user):
    response = client.post(
        reverse("admin:login"),
        dict(
            username=admin_user.username,
            password="password",
            next=reverse("admin:index"),
        ),
    )
    assert response.status_code == 302
    assert response.url.startswith(reverse("admin:index"))
