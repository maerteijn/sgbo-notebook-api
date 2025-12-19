from django.db import models
from django.utils import timezone
from rest_framework import fields, serializers

from .models import Notebook

DjangoModel = type[models.Model]
SerializerFields = str | tuple


class NotebookSerializer(serializers.ModelSerializer):
    url: fields.Field = serializers.HyperlinkedIdentityField(
        source="notebook", view_name="notebook-detail"
    )
    entity_labels: fields.Field = serializers.ListField(read_only=True)

    class Meta:
        model: DjangoModel = Notebook
        fields: SerializerFields = "__all__"
        extra_kwargs: dict = {"body": {"read_only": True}}


class NotebookExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model: DjangoModel = Notebook
        fields: SerializerFields = ("extra",)
        extra_kwargs: dict = {"extra": {"initial": {}}}


class NotebookListSerializer(NotebookSerializer):
    class Meta(NotebookSerializer.Meta):
        fields: SerializerFields = (
            "url",
            "created",
            "modified",
            "title",
            "body",
            "source_id",
        )


class NotebookCreateSerializer(NotebookSerializer):
    class Meta:
        model: DjangoModel = Notebook
        exclude: tuple = ("entities",)  # will be auto-created with a NLP, see .save()
        extra_kwargs: dict = {
            "extra": {"initial": {}},
            "source_date": {"initial": lambda: timezone.localtime().date().isoformat()},
        }

    def to_representation(self, data):
        return NotebookSerializer(context=self.context).to_representation(data)

    def validate(self, attrs):
        instance = self.Meta.model(**attrs)
        instance.full_clean()
        return attrs
