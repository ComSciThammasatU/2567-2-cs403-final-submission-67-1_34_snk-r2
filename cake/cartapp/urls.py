from django.urls import path
from cartapp import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'), 
    path('confirm/', views.confirm_order, name='confirm_order'),
    path('order_history/', views.order_history, name='order_history'),
    path('admin_dashboard/manage_orders/', views.manage_orders, name='manage_orders'),
    path('api/admin_dashboard/sales/monthly/', views.sales_sum, name='monthly_sales_by_year'),
    path('admin_dashboard/sales/', views.sales_dashboard, name='sales_dashboard'),

]