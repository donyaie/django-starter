from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .uuid import create_short_uuid


class BaseModel(models.Model):
    """
        Base Model for created_at, updated_at fields to all models.

    """
    suid = models.CharField(max_length=36, default=create_short_uuid,
                            unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeletableModel(models.Model):
    """
        Model for deletable entities.

    """
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    class Meta:
        abstract = True


class BaseGenericRelationModel(models.Model):
    """
    The base model for managing the generic relations of models.

    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        abstract = True


class NullableBaseGenericRelationModel(models.Model):
    """
    The base model for managing the nullable generic relations of models.

    """
    content_type = models.ForeignKey(ContentType, null=True, blank=True,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    class Meta:
        abstract = True
