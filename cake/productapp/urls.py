from django.urls import path
from productapp import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cakes/', views.show_products, name='show_products'),
    path("cakes/<int:pk>/", views.product_detail, name="product_detail"),
]