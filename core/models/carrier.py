from django.db import models

from ..validators import alphanumeric

class Carrier(models.Model):
    carrier = models.CharField(unique=True, max_length=30, validators=[alphanumeric])
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm_carrier'
    
    def __str__(self) -> str:
        return f'Carrier: {self.id}_{self.carrier}'