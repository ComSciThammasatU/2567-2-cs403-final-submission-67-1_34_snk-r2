from django.contrib import admin
from cartapp.models import Cart, CartItem, Order, OrderItem

# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity', 'message', 'total_price')
    search_fields = ['product__name']
    list_filter = ('size',)

    def user_phone(self, obj):
        return obj.user.phone
    user_phone.admin_order_field = 'user__phone'
    user_phone.short_description = 'User Phone'

class CartAdmin(admin.ModelAdmin):
   
    list_display = ('user', 'created_at')
    search_fields = ['user__phone', 'user__first_name', 'user__last_name']

    def user_phone(self, obj):
        return obj.user.phone
    user_phone.admin_order_field = 'user__phone'
    user_phone.short_description = 'User Phone'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user__first_name','delivery_date','delivery_method', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'delivery_method']
    search_fields = ['user__phone', 'addressname']
    ordering = ['-created_at']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'size']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CartItem, CartItemAdmin) 
admin.site.register(Cart, CartAdmin)

