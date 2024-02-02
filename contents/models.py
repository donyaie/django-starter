from django.contrib.auth import get_user_model
from django.db import models

from core.models import (BaseModel, DeletableModel, NullableBaseGenericRelationModel)


class Content(BaseModel, DeletableModel, NullableBaseGenericRelationModel):
    user = models.ForeignKey(get_user_model(), related_name='contents',on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.suid


class Image(Content):
    content = models.ImageField()
