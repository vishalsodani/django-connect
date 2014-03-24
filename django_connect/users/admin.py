from django.contrib import admin

from .models import User
from .admin_forms import UserAdminForm


class UserAdmin(admin.ModelAdmin):
	form = UserAdminForm


admin.site.register(User, UserAdmin)