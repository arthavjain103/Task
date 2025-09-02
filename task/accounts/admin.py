from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'address_line1', 'city', 'state', 'pincode', 'user_type')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
