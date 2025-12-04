from django.contrib import admin

from .models import Notebook

__all__ = ("NotebookAdmin",)


@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    pass
