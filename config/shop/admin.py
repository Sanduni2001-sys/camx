
# Register your models here.
from django.contrib import admin
from .models import Product, CartItem, ServiceRequest,RentItem


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(RentItem)
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        'service_name',
        'full_name',
        'phone',
        'email',
        'preferred_date',
        'created_at'
    )
    search_fields = ('full_name', 'phone', 'email', 'service_name')
    list_filter = ('service_name', 'created_at')