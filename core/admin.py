from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User, Carrier, Team

# Register your models here.
fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)
admin.site.register(Carrier)
admin.site.register(Team)




