from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ('total',)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'customer', 'date', 'total_amount', 'payment_status')
    list_filter = ('date', 'payment_method', 'payment_status')
    search_fields = ('invoice_number', 'customer__name')
    inlines = [InvoiceItemInline]
    readonly_fields = ('subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'balance')

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem)