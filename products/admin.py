from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'tax_percentage', 'discount', 'stock')
    search_fields = ('name', 'hsn_code')
    list_filter = ('created_at',)
    ordering = ('name',)
    readonly_fields = ('selling_price',)

admin.site.register(Product, ProductAdmin)