from django.db import models
from django.conf import settings
from productapp.models import Product

# Create your models here.

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'จัดส่ง'),
        ('pickup', 'รับเองที่ร้าน'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    addressname = models.TextField(default="ไม่ระบุ")
    address = models.TextField()
    delivery_date = models.DateField()
    delivery_time = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    cancel_reason = models.TextField(blank=True, null=True)

    slip=models.ImageField(upload_to="orders",blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.first_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.PositiveIntegerField()  # 1, 2, 3 ปอนด์
    message = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity} ({self.size} ปอนด์)"
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.PositiveIntegerField()  # ขนาดเค้ก เช่น 1, 2, 3 (ปอนด์)
    message = models.TextField(blank=True, null=True)  # ข้อความบนเค้ก

    def __str__(self):
        return f"{self.product.name} x {self.quantity} ({self.size} ปอนด์)"
    
    @property
    def total_price(self):
        return self.product.get_price(self.size) * self.quantity