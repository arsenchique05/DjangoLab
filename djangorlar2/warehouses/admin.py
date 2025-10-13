from django.contrib import admin
from .models import Warehouse, Box

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name', 'location')

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'weight', 'warehouse', 'is_deleted')
    list_filter = ('color', 'is_deleted')
    search_fields = ('color',)
