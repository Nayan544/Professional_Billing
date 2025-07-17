from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    stock = models.PositiveIntegerField(default=0)
    hsn_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def selling_price(self):
        return self.price - (self.price * self.discount / 100)