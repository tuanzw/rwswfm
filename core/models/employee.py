from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.validators import alphanumeric, numeric_only
from core.models.user import User

class EmployeeManager(models.Manager):
    def get_queryset(self):
        # Automatically joins the User table on EVERY Employee query by default
        return super().get_queryset().select_related('user')

class Employee(models.Model):
    # Attach the optimized manager (Auto-joins User table)
    objects = EmployeeManager()

    # Fallback manager (No joins, completely raw table queries)
    raw_objects = models.Manager()

    class GenderChoice(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    # This acts as both the link and the primary identification
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    gender = models.CharField(max_length=10, verbose_name='Gender', choices=GenderChoice.choices)
    dob = models.DateField(verbose_name='Date of Birth')
    id_number = models.CharField(max_length=20, unique=True, verbose_name='ID Number', validators=[numeric_only])
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=20, verbose_name='Created By')
    updated_by = models.CharField(max_length=20, verbose_name='Updated By')

    teams = models.ManyToManyField(
        'Team',
        through='EmployeeTeam',
        related_name='employees',
        verbose_name='Assigned Teams'
    )

    class Meta:
        db_table = 'm_employee'
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user.username} - {self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.updated_date = timezone.now()
        super().save(*args, **kwargs)

class EmployeeTeam(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_teams')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='team_employees')

    class Meta:
        db_table = 'm_employee_team'
        verbose_name = "Employee Team Membership"
        verbose_name_plural = "Employee Team Memberships"
        unique_together = ('employee', 'team')
        # ordering = ['employee__code', 'team__name']