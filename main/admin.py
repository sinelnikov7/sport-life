from django.contrib import admin
from .models import User, ConfirmCode, Setting


admin.site.register(User)
admin.site.register(ConfirmCode)
admin.site.register(Setting)
