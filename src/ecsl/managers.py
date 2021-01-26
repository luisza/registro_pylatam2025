from django.db import models


class CurrentEventManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(event__current=True)