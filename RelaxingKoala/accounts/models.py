from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    is_customer = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='users_in_group',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='users_with_permissions',
        related_query_name='user'
    )

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loyalty_points = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default='Unnamed Customer')
    
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    salary = models.FloatField()
    hire_date = models.DateField()

class KitchenStaff(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)
