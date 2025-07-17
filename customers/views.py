from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 10

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ['name', 'email', 'phone', 'address', 'gstin']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')

class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['name', 'email', 'phone', 'address', 'gstin']
    template_name = 'customers/customer_form.html'
    success_url = reverse_lazy('customer-list')