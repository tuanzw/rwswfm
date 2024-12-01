from django.db import models


from . import Employee, User


class Attendance(models.Model):
    empid = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    site_id = models.CharField(max_length=30)
    sys_intime = models.TimeField()
    sys_outtime = models.TimeField()
    sup_intime = models.TimeField(null=True)
    sup_outtime = models.TimeField(null=True)
    duration = models.DurationField()
    workday = models.DecimalField(max_digits=3, decimal_places=1)
    ot = models.SmallIntegerField(null=True)
    ot_night = models.SmallIntegerField(null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    dayoff = models.BooleanField(default=False)
    period = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.empid}_{self.date}'