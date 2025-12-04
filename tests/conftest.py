import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from sgbo_notebook_api.models import Notebook, SourceId


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def notebook():
    notebook = Notebook.objects.create(
        title="My Notebook",
        body="My test body",
        source_id=SourceId.T112,
        source_date=timezone.now().date(),
    )
    return notebook
