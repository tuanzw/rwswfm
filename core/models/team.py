from django_extensions.db.fields import AutoSlugField
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        db_table = 'm_team'

    def __str__(self):
        return self.name