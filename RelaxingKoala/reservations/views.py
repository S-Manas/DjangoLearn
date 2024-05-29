from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm

@login_required
def reserve_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user.customer
            reservation.save()
            messages.success(request, 'Table reserved successfully!')
            return redirect('order_detail', order_id=reservation.order.id if reservation.order else 'order_list')
        else:
            messages.error(request, 'Failed to reserve table. Please check the form data.')
    else:
        form = ReservationForm()
    return render(request, 'reservations/reserve.html', {'form': form})