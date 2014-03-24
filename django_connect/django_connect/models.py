from django.db import models


class AbstractModel(models.Model):

    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True