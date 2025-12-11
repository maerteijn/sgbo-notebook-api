import json

import pytest
from django.forms.models import model_to_dict
from django.urls import reverse
from django.utils import timezone

from sgbo_notebook_api.models import SourceId


@pytest.mark.django_db
def test_index_view(api_client):
    expected_index_data = {
        "notebooks": "http://testserver/notebooks/",
    }
    response = api_client.get(reverse("api-root"))
    assert response.status_code == 200
    assert response.data == expected_index_data


@pytest.mark.django_db
def test_notebooks_api__list(api_client, notebook):
    response = api_client.get(reverse("notebook-list"))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == notebook.title


@pytest.mark.django_db
def test_notebooks_api__get(api_client, notebook):
    response = api_client.get(reverse("notebook-detail", kwargs=dict(pk=notebook.pk)))
    assert response.status_code == 200
    assert response.data["title"] == notebook.title
    assert response.data["created"] == timezone.localtime(notebook.created).isoformat()
    assert (
        response.data["modified"] == timezone.localtime(notebook.modified).isoformat()
    )


@pytest.mark.django_db
def test_notebooks_api__create(api_client):
    response = api_client.post(
        reverse("notebook-list"),
        data=dict(
            title="My Notebook",
            body="2 mannen in een witte auto",
            source_id=SourceId.T112,
            source_date=timezone.now().date().isoformat(),
        ),
    )
    assert response.status_code == 201

    notebook_pk = response.data["id"]
    response = api_client.get(reverse("notebook-detail", kwargs=dict(pk=notebook_pk)))
    assert response.status_code == 200
    assert response.data["entity_labels"] == ["SIGNAL"]


@pytest.mark.django_db
def test_notebooks_api__put(api_client, notebook):
    new_title = "Another title"
    assert notebook.title != new_title  # guard

    data = model_to_dict(notebook) | dict(title=new_title)

    response = api_client.put(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk)),
        data,
        format="json",
    )
    assert response.status_code == 200

    notebook.refresh_from_db()
    assert notebook.title == new_title


@pytest.mark.django_db
def test_notebooks_api__patch(api_client, notebook):
    new_title = "Another title"
    assert notebook.title != new_title  # guard

    response = api_client.patch(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk)),
        dict(title=new_title),
        format="json",
    )
    assert response.status_code == 200

    notebook.refresh_from_db()
    assert notebook.title == new_title


@pytest.mark.django_db
def test_notebooks_api__patch_body_is_read_only(api_client, notebook):
    current_body = notebook.body
    response = api_client.patch(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk)),
        dict(body="I am an updated body"),
    )
    assert response.status_code == 200

    notebook.refresh_from_db()
    assert notebook.body == current_body


@pytest.mark.django_db
def test_notebooks_api__patch_entities_error(api_client, notebook):
    response = api_client.patch(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk)),
        dict(entities="""{"invalid": "json"}"""),
    )
    # Can't update with invalid JSON
    assert response.status_code == 400


@pytest.mark.django_db
def test_notebooks_api__patch_entities_success(api_client, notebook):
    entities = [{"text": "18:57", "start_char": 0, "end_char": 4, "label": "TIME"}]
    response = api_client.patch(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk)),
        dict(entities=json.dumps(entities)),
    )
    assert response.status_code == 200

    # Make sure the given entities are stored in the database
    notebook.refresh_from_db()
    assert notebook.entities == entities

    notebook_pk = response.data["id"]
    response = api_client.get(reverse("notebook-detail", kwargs=dict(pk=notebook_pk)))
    assert response.status_code == 200
    assert response.data["entity_labels"] == ["TIME"]


@pytest.mark.django_db
def test_notebooks_api__delete(api_client, notebook):
    response = api_client.delete(
        reverse("notebook-detail", kwargs=dict(pk=notebook.pk))
    )
    assert response.status_code == 204

    response = api_client.get(reverse("notebook-list"))
    assert response.status_code == 200
    assert response.data == []
