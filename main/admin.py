from django.contrib import admin
from .models import User, ConfirmCode


admin.site.register(User)
admin.site.register(ConfirmCode)
