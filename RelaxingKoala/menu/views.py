from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MenuItem, Order, Customer
from .forms import OrderForm, PaymentForm, ReservationForm, MenuItemForm
from reservations.models import Reservation
from .utils import attach_customer_to_order, increment_points
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db import transaction
from reservations.models import Table



# Create your views here.
def order_menu(request):
    menu_items = MenuItem.objects.filter(available=True)
    return render(request, 'menu/order.html', {'menu_items': menu_items})

def checkout_order(request):
    total_cost = 0  # Initialize total_cost to 0
    if request.method == 'POST':
        order_form = OrderForm(request.POST, user=request.user)
        payment_form = PaymentForm(request.POST)
        if order_form.is_valid() and payment_form.is_valid():
            with transaction.atomic():
                order = order_form.save(commit=False)

                # Calculate Total
                ordered_menu_items = order_form.cleaned_data.get('ordered_menu_items')
                total_cost = sum(item.price for item in ordered_menu_items)

                # Process ordered menu items and update inventory
                for item in ordered_menu_items:
                    menu_item = MenuItem.objects.get(pk=item.pk)
                    menu_item.inventory_item.quantity -= 1  # Assuming each menu item reduces inventory count by 1
                    menu_item.inventory_item.save()

                # Attach the order to the user if logged in, otherwise proceed as anonymous
                if request.user.is_authenticated:
                    customer, created = Customer.objects.get_or_create(user=request.user)
                    order.customer = customer

                    # Check for existing reservations
                    user_reservations_today = Reservation.get_user_reservations_today(request.user)

                    if user_reservations_today.exists():
                        default_table = user_reservations_today.first()
                    else:
                        # Assign the first available table
                        default_table = Table.objects.first()
                        if not default_table:
                            messages.error(request, 'No tables available for reservation.')
                            return redirect('menu:checkout_order')  # Redirect back to the checkout page

                        reservation = Reservation.objects.create(
                            customer=customer,
                            start_time=timezone.now(),
                            end_time=timezone.now() + timezone.timedelta(hours=1),
                            table=default_table
                        )

                    order.save()

                    # Increment loyalty points by 10 for every product ordered
                    customer.loyalty_points += 10 * len(ordered_menu_items)
                    customer.save()

                    # Proceed with payment
                    payment = payment_form.save(commit=False)
                    payment.amount = total_cost
                    payment.save()

                    return redirect('menu:order_detail', order_id=order.id)
                else:
                    order.save()

                    # Proceed with payment without customer
                    payment = payment_form.save(commit=False)
                    payment.amount = total_cost
                    payment.save()

                    return redirect('menu:order_detail', order_id=order.id)
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        order_form = OrderForm(user=request.user)
        payment_form = PaymentForm()
        # For GET requests, total_cost should be 0 since no order has been placed yet

    return render(request, 'menu/checkout.html', {
        'order_form': order_form,
        'payment_form': payment_form,
        'total_cost': total_cost,
        'user': request.user
    })

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    try:
        reservation = Reservation.objects.get(order=order)
        table = reservation.table
    except Reservation.DoesNotExist:
        reservation = None
        table = None
    
    context = {
        'order': order,
        'reservation': reservation,
        'table': table,
    }
    return render(request, 'menu/order_detail.html', context)

def add_menu_item(request):
    if not request.user.is_staff_member:
        return redirect('home')  # Redirect non-staff to home page
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirect to menu page after adding item
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})