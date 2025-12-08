from rest_framework import viewsets

from .models import Notebook
from .serializers import (
    NotebookCreateSerializer,
    NotebookListSerializer,
    NotebookSerializer,
)


class NotebookViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        match self.action:
            case "create":
                return NotebookCreateSerializer
            case "list":
                return NotebookListSerializer
            case _:
                return NotebookSerializer

    def get_queryset(self):
        return Notebook.objects.all()
