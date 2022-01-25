from django.contrib import admin
from .models import Responses
# Register your models here.


@admin.register(Responses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ['u_id', 'q_id', 'description', 'file_path', 'created_at', 'updated_at', 'is_active']
