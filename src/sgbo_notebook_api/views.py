from django.views.generic import TemplateView
from rest_framework import viewsets
from spacy import displacy

from .models import Notebook
from .nlp import NLPUtility
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
