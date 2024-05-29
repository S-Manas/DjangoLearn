from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import User, Customer, Staff
from django.utils import timezone

@receiver(pre_delete, sender=User)
def delete_related_profiles(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'customer'):
            instance.customer.delete()
    except Customer.DoesNotExist:
        pass

    try:
        if hasattr(instance, 'staff'):
            staff_instance = instance.staff
            if hasattr(staff_instance, 'kitchenstaff'):
                staff_instance.kitchenstaff.delete()
            staff_instance.delete()
    except Staff.DoesNotExist:
        pass

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_customer:
            Customer.objects.get_or_create(user=instance, defaults={'name': instance.name})
        if instance.is_staff_member:
            Staff.objects.get_or_create(user=instance, defaults={'position': 'default position', 'salary': 0.0, 'hire_date': timezone.now()})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_customer:
        customer, created = Customer.objects.get_or_create(user=instance)
        if not created:  # Only update the name if the Customer already exists
            customer.name = instance.name
            customer.save()
    if instance.is_staff_member:
        staff, created = Staff.objects.get_or_create(user=instance)
        if not created:
            staff.save()