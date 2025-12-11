from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from spacy import displacy

from .models import Notebook
from .nlp import NLPUtility
from .serializers import (
    NotebookCreateSerializer,
    NotebookExtraSerializer,
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
            case "update_extra":
                return NotebookExtraSerializer
            case _:
                return NotebookSerializer

    def get_queryset(self):
        return Notebook.objects.all()

    @action(methods=["get", "post"], detail=True)
    def update_extra(self, request, pk=None):
        notebook = self.get_object()

        match request.method:
            case "GET":
                serializer = NotebookExtraSerializer(notebook, read_only=True)  # type: ignore[var-annotated]
            case "POST":
                serializer = NotebookExtraSerializer(notebook, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return Response(serializer.data)


class NLPDebugView(TemplateView):
    template_name = "nlp_debug.html"

    def post(self, request, *args, **kwargs):
        text = request.POST["text"]
        nlp_utility = NLPUtility(text)

        context = self.get_context_data(**kwargs)
        extra_context = dict(
            text=request.POST["text"],
            html_ent=displacy.render(nlp_utility.doc, style="ent"),
            html_dep=displacy.render(list(nlp_utility.doc.sents), style="dep"),
        )

        return self.render_to_response(context | extra_context)
