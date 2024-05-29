from django.contrib import admin
from .models import User, Customer, Staff, KitchenStaff

class UserAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

admin.site.register(User, UserAdmin)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(KitchenStaff)
