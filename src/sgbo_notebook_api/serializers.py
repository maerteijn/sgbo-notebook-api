from rest_framework import serializers

from .models import Notebook


class NotebookSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        source="notebook", view_name="notebook-detail"
    )

    class Meta:
        model = Notebook
        fields = "__all__"
        extra_kwargs: dict = {"extra": {"initial": {}}}


class NotebookEditSerializer(NotebookSerializer):
    class Meta(NotebookSerializer.Meta):
        extra_kwargs = {"body": {"read_only": True}}
