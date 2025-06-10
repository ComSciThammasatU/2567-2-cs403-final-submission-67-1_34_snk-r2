from django.urls import path
from commentapp import views

urlpatterns = [
    path('addcomment/<int:product_id>/', views.add_comment, name='add_comment'),
]