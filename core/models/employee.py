from django.db import models

from ..validators import numeric
from . import Vendor


class Employee(models.Model):
    empid = models.CharField(max_length=30, unique=True)
    pin = models.CharField(max_length=15, unique=True, validators=[numeric])
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='employees')

    class Meta:
        db_table = 'm_employee'

    def __str__(self):
        return self.empid