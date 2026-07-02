from django.db import models
from django.utils import timezone
from core.models.employee import Employee
from core.validators import alphanumeric

class TeamManager(models.Manager):
    def get_queryset(self):
        # PERFORMANCE SHIELD: Prefetches subteams, leaders, and user profiles 
        return super().get_queryset().prefetch_related(
            'subteams',
            'leader__user'
        )

class Team(models.Model):
    objects = TeamManager()
    raw_objects = models.Manager()  # Fallback manager for raw queries

    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[alphanumeric],
        verbose_name='Team')
    leader = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams',
        verbose_name="Team Leader"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Is Active")
    
    # Self-referential Many-to-Many field for network-style subteams
    subteams = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='parent_teams',
        db_table='m_team_subteams',
        verbose_name="Subteams"
    )
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=20, verbose_name='Created By')
    updated_by = models.CharField(max_length=20, verbose_name='Updated By')

    class Meta:
        db_table = 'm_team'
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name = self.name.strip().upper()
        if not self._state.adding:
            self.updated_date = timezone.now()
        super().save(*args, **kwargs)