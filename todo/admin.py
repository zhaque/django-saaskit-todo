from django.contrib import admin
from todo.models import Item, User, List

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'list', 'priority', 'due_date')
    list_filter = ('list',)
    ordering = ('priority',)
    search_fields = ('name',)


admin.site.register(List)
admin.site.register(Item,ItemAdmin)