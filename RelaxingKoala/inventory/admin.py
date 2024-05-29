from django.contrib import admin
from .models import Inventory, Supplier, Payment
# Register your models here.
admin.site.register(Inventory)
admin.site.register(Supplier)
admin.site.register(Payment)