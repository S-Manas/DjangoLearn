from django.db import models
from django.apps import apps
from accounts.models import Customer
# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    available = models.BooleanField(default=True)
    inventory_item = models.ForeignKey(
        'inventory.Inventory', 
        on_delete=models.CASCADE,
        related_name='menu_items',
        default=1
    )
    def __str__(self):
        return self.name
    
    def inventory(self):
        Inventory = apps.get_model('inventory', 'Inventory')
        return Inventory.objects.get(id=self.inventory_item_id)

class Order(models.Model):
    ordered_menu_items = models.ManyToManyField(MenuItem)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        total = sum(order_line.price for order_line in self.orderline_set.all())
        return total
    
    def __str__(self):
        return f"Order {self.id} for {self.customer}"

class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

class Payment(models.Model):
    credit_card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment of {self.amount}'