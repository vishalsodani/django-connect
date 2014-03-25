from django.contrib import admin

from .models import User, Email, NewEmail #, Phone, NewPhone


class UserAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'birthday', 'gender', 'language', 'timezone', 'is_seller', 'is_staff', 'is_active', 'username', 'password', 'created_on', 'modified_on', 'last_login',)
    readonly_fields = ('username', 'password', 'created_on', 'modified_on', 'last_login',)

class EmailAdmin(admin.ModelAdmin):
    pass

class NewEmailAdmin(admin.ModelAdmin):
    pass



admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(NewEmail, NewEmailAdmin)


# class PhoneAdmin(admin.ModelAdmin):
#     pass

# class NewPhoneAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(Phone, PhoneAdmin)
# admin.site.register(NewPhone, NewPhoneAdmin)