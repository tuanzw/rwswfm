from django.db import models

from core.validators import alphanumeric

class Carrier(models.Model):
    carrier = models.CharField(
        max_length=30,
        unique=True,
        validators=[alphanumeric],
        verbose_name="Carrier"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Name"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )
    address = models.CharField(max_length=300, verbose_name="Address")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'm_carrier'
        verbose_name = "Carrier"
        verbose_name_plural = "Carriers"
        ordering = ['carrier']
    
    def __str__(self) -> str:
        return f'Carrier: {self.carrier}'
    
    def save(self, *args, **kwargs):
        self.carrier = self.carrier.strip().upper()
        super().save(*args, **kwargs)