from functools import partial

import jsonschema
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .nlp import NLPUtility
from .schemas import ENTITIES_SCHEMA


def validate_json_data_with_schema(value, schema=ENTITIES_SCHEMA):
    try:
        jsonschema.validate(instance=value, schema=schema)
    except (jsonschema.exceptions.SchemaError, jsonschema.ValidationError) as e:
        raise ValidationError(e.message)


class SourceId(models.TextChoices):
    T112 = "112", _("112")
    T09008844 = "0900-8844", _("0900-8844")
    MA = "Misdaad Anoniem", _("Misdaad Anoniem")
    SOCIALMEDIA = "Social Media", _("Social Media")


class Prio(models.TextChoices):
    P1 = "P1", _("P1")
    P2 = "P2", _("P2")
    P3 = "P3", _("P3")
    P4 = "P4", _("P4")
    P5 = "P5", _("P5")


class Notebook(models.Model):
    """
    A Django model representing a notebook
    """

    created = models.DateTimeField(
        verbose_name=_("created"), name="created", auto_now_add=True, editable=False
    )
    modified = models.DateTimeField(
        verbose_name=_("modified"), name="modified", auto_now=True, editable=False
    )

    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("The title of this notebook"),
        max_length=255,
        null=False,
        blank=False,
    )
    desctipion = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description, which can be in any format you like"),
        null=False,
        blank=True,
    )

    body = models.TextField(
        verbose_name=_("Notebook Body"),
        help_text=_("The body of the notebook as plain text"),
        null=False,
        blank=False,
    )

    prio = models.CharField(
        max_length=255,
        choices=Prio,
        default=Prio.P1,
    )
    source_id = models.CharField(
        max_length=255,
        choices=SourceId,
        default=SourceId.T112,
    )
    source_date = models.DateField(verbose_name=_("source date"))

    entities = models.JSONField(
        verbose_name=_("Entities"),
        help_text=_("A JSON Field representing entities"),
        null=False,
        blank=True,
        default=dict,
        validators=[partial(validate_json_data_with_schema, schema=ENTITIES_SCHEMA)],
    )
    extra = models.JSONField(
        verbose_name=_("Extra data"),
        help_text=_("A JSON Field with extra data to store"),
        null=False,
        blank=True,
        default=dict,
    )

    class Meta:
        verbose_name = _("Notebook")
        verbose_name_plural = _("Notebooks")
        ordering = ("-created",)

    def __str__(self) -> str:
        return self.title

    @property
    def entity_labels(self) -> list:
        return list({x["label"] for x in self.entities})

    def save(self, *args, **kwargs):
        # Generate entities when creating new notebooks
        if self._state.adding:
            nlp_utility = NLPUtility(text=self.body)
            self.entities = list(nlp_utility.entities)
        super().save(*args, **kwargs)
