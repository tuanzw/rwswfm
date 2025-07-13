from django.urls import include, path
from core.urls.tasks import add_task

urlpatterns = [
    path('', add_task, name='home'),
    path('teams/', include('core.urls.teams')),
    path('carriers/', include('core.urls.carriers')),
    path('users/', include('core.urls.users')),
    path('tasks/', include('core.urls.tasks')),
]