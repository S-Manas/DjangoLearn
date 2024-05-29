from django.db import models
from django.utils import timezone
from accounts.models import Customer
from menu.models import Order
from datetime import timedelta

def default_end_time():
    return timezone.now() + timedelta(hours=1)

class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.number} (Capacity: {self.capacity})"

class Reservation(models.Model):
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=default_end_time)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, default=None, blank=True, null=True)
    reserved_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=default_end_time)

    @property
    def is_expired(self):
        return self.expires_at < timezone.now()
    
    @classmethod
    def get_user_reservations_today(cls, user):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        return cls.objects.filter(customer=user.customer, start_time__gte=today_start, start_time__lt=today_end)
