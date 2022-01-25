from django.contrib import admin
from .models import Queries
# Register your models here.


@admin.register(Queries)
class QueriesAdmin(admin.ModelAdmin):
    list_display = ['u_id', 'title', 'description', 't_id', 'created_at', 'updated_at',
                    'is_active']
