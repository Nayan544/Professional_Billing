from django.contrib import admin
from django.urls import path, include
from accounts.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('customers/', include('customers.urls')),
    path('products/', include('products.urls')),
    path('invoices/', include('invoices.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Django's built-in auth URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]