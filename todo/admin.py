from django.contrib import admin
from .models import TODO


class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(TODO, TodoAdmin)

