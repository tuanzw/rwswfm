from django_extensions.db.fields import AutoSlugField
from django.db import models
from . import Task, User


class Assignment(models.Model):

    class StatusChoice(models.TextChoices):
        RELEASED = 'Released', 'Released'
        INPROGRESS = 'InProgress', 'InProgress'
        COMPELETED = 'Completed', 'Completed'
        CANCELLED = 'Cancelled', 'Cancelled'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    empid = models.CharField(max_length=50)
    rfid = models.CharField(max_length=50, blank=True)
    buff = models.CharField(max_length=50, blank=True)
    listid = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=StatusChoice, default=StatusChoice.RELEASED)
    estimate_mi = models.PositiveIntegerField(default=30)
    actual_mi = models.PositiveIntegerField(default=0)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(null=True)
    createdby = models.CharField(max_length=150, blank=True)
    updatedby = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 't_assignment'


    def __str__(self):
        return f'{self.empid}_{self.task.name}_{self.status}'
