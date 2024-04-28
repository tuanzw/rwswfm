from django_extensions.db.fields import AutoSlugField
from django.db import models
from . import Team


class Task(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks')
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        db_table = 'm_task'

    def __str__(self):
        return self.name