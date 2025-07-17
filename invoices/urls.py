from django.urls import path
from .views import (InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceUpdateView, 
                   add_invoice_item, generate_pdf, export_excel)

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list'),
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('<int:pk>/add-item/', add_invoice_item, name='add-invoice-item'),
    path('<int:pk>/pdf/', generate_pdf, name='generate-pdf'),
    path('export-excel/', export_excel, name='export-excel'),
]