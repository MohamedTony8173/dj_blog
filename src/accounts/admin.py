from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['full_name','username','email','is_active','is_superuser']
    fieldsets = (
        (None, {
            "fields": (
                'password',
            ),
        }),
        
        ('Information', {
            "fields": (
                'first_name','last_name','username','email'
            ),
        }),
        
        ('Permissions', {
            "fields": (
                'is_active','is_admin','is_superuser','is_superadmin','is_staff'
            ),
        }),
        
        ('group', {
            "fields": (
                'groups', 'user_permissions'

            ),
        }),
      
    )

admin.site.register(CustomUser,CustomUserAdmin)    
