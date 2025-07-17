from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
from io import BytesIO

from .models import Invoice, InvoiceItem
from customers.models import Customer
from products.models import Product

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoices/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10

class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    fields = ['customer', 'due_date', 'payment_method', 'notes']
    template_name = 'invoices/invoice_create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Invoice created successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('invoice-detail', kwargs={'pk': self.object.pk})

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoices/invoice_detail.html'
    context_object_name = 'invoice'

class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    fields = ['customer', 'due_date', 'payment_method', 'notes']
    template_name = 'invoices/invoice_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Invoice updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('invoice-detail', kwargs={'pk': self.object.pk})
    
def add_invoice_item(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        
        product = get_object_or_404(Product, pk=product_id)
        
        InvoiceItem.objects.create(
            invoice=invoice,
            product=product,
            quantity=quantity,
            unit_price=product.selling_price,
            tax_percentage=product.tax_percentage,
            discount_percentage=product.discount,
            total=quantity * product.selling_price
        )
        
        # Update invoice totals
        update_invoice_totals(invoice)
        
        messages.success(request, 'Item added successfully!')
        return redirect('invoice-detail', pk=pk)
    
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'invoices/add_item.html', {'invoice': invoice, 'products': products})

def update_invoice_totals(invoice):
    items = invoice.items.all()
    subtotal = sum(item.total for item in items)
    tax_amount = sum(item.total * item.tax_percentage / 100 for item in items)
    discount_amount = sum(item.total * item.discount_percentage / 100 for item in items)
    
    invoice.subtotal = subtotal
    invoice.tax_amount = tax_amount
    invoice.discount_amount = discount_amount
    invoice.total_amount = subtotal + tax_amount - discount_amount
    invoice.balance = invoice.total_amount - invoice.paid_amount
    invoice.save()

def generate_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    template_path = 'invoices/invoice_pdf.html'
    context = {'invoice': invoice}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating PDF')
    return response

def export_excel(request):
    invoices = Invoice.objects.all()
    data = []
    
    for invoice in invoices:
        data.append({
            'Invoice Number': invoice.invoice_number,
            'Customer': invoice.customer.name,
            'Date': invoice.date,
            'Total Amount': invoice.total_amount,
            'Paid Amount': invoice.paid_amount,
            'Balance': invoice.balance,
            'Payment Status': 'Paid' if invoice.payment_status else 'Pending',
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, sheet_name='Invoices', index=False)
    writer.save()
    output.seek(0)
    
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=invoices.xlsx'
    return response