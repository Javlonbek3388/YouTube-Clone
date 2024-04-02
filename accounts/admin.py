from django.contrib import admin
from .models import User, UserConfirmation
# Register your models here.

admin.site.register(User)
admin.site.register(UserConfirmation)