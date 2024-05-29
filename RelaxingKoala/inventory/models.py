from django.db import models
from django.apps import apps

# Create your models here.
class Inventory(models.Model):
    item_name = models.CharField(max_length=255, default="Unknown")
    #menu_item = models.OneToOneField(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    def __str__(self):
        return self.item_name
    
    def menu_items(self):
        MenuItem = apps.get_model('menu', 'MenuItem')
        return MenuItem.objects.filter(inventory_item=self)


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()

class Payment(models.Model):
    order = models.OneToOneField('menu.Order', on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)