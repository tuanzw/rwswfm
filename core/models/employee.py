from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.validators import alphanumeric, numeric_only

class Employee(models.Model):
    class Gender(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')


    code = models.CharField(max_length=20, unique=True, verbose_name='Employee Code', validators=[alphanumeric])
    name = models.CharField(max_length=200, verbose_name='Employee Name')
    gender = models.CharField(max_length=10, verbose_name='Gender', choices=Gender.choices)
    dob = models.DateField(verbose_name='Date of Birth')
    id_number = models.CharField(max_length=20, unique=True, verbose_name='ID Number', validators=[numeric_only])
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=50, verbose_name='Created By')
    updated_by = models.CharField(max_length=50, verbose_name='Updated By')

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
        ordering = ['code']

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
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