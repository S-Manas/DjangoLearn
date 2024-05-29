from django import forms
from .models import MenuItem, Order, Payment
from reservations.models import Reservation


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'inventory_item']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_menu_items']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['ordered_menu_items'].widget = forms.CheckboxSelectMultiple()
        self.fields['ordered_menu_items'].queryset = MenuItem.objects.all()

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['credit_card_number', 'expiration_date']

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id']  # Assuming you want to select existing reservations by ID
        widgets = {'id': forms.RadioSelect}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].queryset = kwargs.pop('queryset', Reservation.objects.none())