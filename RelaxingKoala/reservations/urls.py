from django.urls import path
from .views import reserve_table

urlpatterns = [
    path('reserve/', reserve_table, name='reserve_table'),
]
