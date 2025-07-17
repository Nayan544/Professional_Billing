from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice
from customers.models import Customer
from products.models import Product

@login_required
def dashboard(request):
    total_invoices = Invoice.objects.count()
    total_customers = Customer.objects.count()
    total_products = Product.objects.count()
    
    recent_invoices = Invoice.objects.order_by('-date')[:5]
    
    context = {
        'total_invoices': total_invoices,
        'total_customers': total_customers,
        'total_products': total_products,
        'recent_invoices': recent_invoices,
    }
    return render(request, 'dashboard/dashboard.html', context)