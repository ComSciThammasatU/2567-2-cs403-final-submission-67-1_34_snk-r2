from django.urls import path
from userapp import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/edit-menu/', views.edit_menu, name='edit_menu'),
    path('admin_dashboard/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('add/', views.add_product, name='add_product'),
    path("toggle-available/<int:pk>/", views.toggle_available, name="toggle_available"),
    path("send_otp/", views.send_otp, name="send_otp"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
]
