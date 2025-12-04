from rest_framework import viewsets

from .models import Notebook
from .serializers import NotebookEditSerializer, NotebookSerializer


class NotebookViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return NotebookEditSerializer
        return NotebookSerializer

    def get_queryset(self):
        return Notebook.objects.all()
