from django.contrib import admin
from .models import Status, Priority, Task


admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Task)
# Register your models here.
