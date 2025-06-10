from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from userapp.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['phone', 'first_name', 'last_name', 'is_active', 'is_staff']
    search_fields = ['phone', 'first_name', 'last_name']  # ค้นหาจาก phone
    ordering = ['phone']
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
# Register your models here.
