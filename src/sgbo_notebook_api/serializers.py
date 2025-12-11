from django.utils import timezone
from rest_framework import serializers

from .models import Notebook


class NotebookSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        source="notebook", view_name="notebook-detail"
    )
    entity_labels = serializers.ListField(read_only=True)

    class Meta:
        model = Notebook
        fields = "__all__"
        extra_kwargs = {"body": {"read_only": True}}


class NotebookExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = ("extra",)
        extra_kwargs: dict = {"extra": {"initial": {}}}


class NotebookListSerializer(NotebookSerializer):
    class Meta(NotebookSerializer.Meta):
        fields = ("url", "created", "modified", "title", "body", "source_id")  # type: ignore[assignment]


class NotebookCreateSerializer(NotebookSerializer):
    class Meta:
        model = Notebook
        exclude = ("entities",)  # will be auto-created with a NLP, see .save()
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
