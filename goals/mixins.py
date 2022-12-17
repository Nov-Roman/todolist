from rest_framework import serializers
from django.db import models
from django.utils import timezone


class ValidationIsDeleteMixin:
    def validate_delete(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Not allowed in deleted")
        return value


class ValidationCheckUserMixin:
    def validate_user(self, value):
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("You not owner")
        return value


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)
