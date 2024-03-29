from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email',  'is_staff', 'is_active', 'date_joined', 'last_login']
    search_fields = ['username', 'email',]
    readonly_fields = ['date_joined']
    ordering = ['-date_joined']

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'phone_number', 'date_joined')}),
        ('Personal info', {'fields': ( 'domain','gender', 'email_verified', 'mobile_verified')}),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_staff', 'is_admin','is_active', 'groups', 'user_permissions')
            }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser,CustomUserAdmin)
