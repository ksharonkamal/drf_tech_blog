from django.contrib import admin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'firstname', 'lastname', 'mobile', 'created_at', 'updated_at',
                    'is_staff', 'is_active', 'is_superuser', 'is_admin']
