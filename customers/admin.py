from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'gstin')
    search_fields = ('name', 'email', 'phone', 'gstin')
    list_filter = ('created_at',)
    ordering = ('name',)

admin.site.register(Customer, CustomerAdmin)