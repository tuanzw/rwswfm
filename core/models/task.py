from django.db import models
from core.validators import alphanumeric

class Task(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[alphanumeric],
        verbose_name="Task"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Is Active"
    )

    class Meta:
        db_table = 'task'
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['name']  # good practice for predictable querysets

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        super().save(*args, **kwargs)
