from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Number of extra empty forms
    readonly_fields = ('price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'email', 'phone', 'ordered_at', 'status', 'total_sum')
    list_filter = ('status', 'ordered_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'email', 'phone')
    inlines = [OrderItemInline, ]  # To allow managing Order Items directly from the Order
    readonly_fields = ('order_number', 'ordered_at', 'total_sum')  # Prevent these fields from being edited

    # This will ensure that the total_sum is recalculated every time related objects are saved in the admin interface.
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.total_sum = sum(item.price for item in form.instance.orderitem_set.all())
        form.instance.save()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('price',)  # The price is computed, so it should be read-only
