from django.db import models
from django.conf import settings
from productapp.models import Product
from cartapp.models import OrderItem

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    commenttext = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    sentiment = models.CharField(max_length=20, blank=True, null=True)  # rec pos / neg
    reply = models.TextField(blank=True, null=True) # use to convert pos / neg to reply text

    def __str__(self):
        return f"{self.user.first_name} on {self.product.name}"