from django.db import models

# Create your models here.

# onepprice mean one pound per price also two three
# is_avaible is about this menu open for sale or not
# in category hav was the ingredient that use to make cake(product) desig in boolean cuz u can do only check list of it
class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    one_pound_price = models.DecimalField(max_digits=10,decimal_places=2)
    two_pound_price = models.DecimalField(max_digits=10,decimal_places=2)
    three_pound_price = models.DecimalField(max_digits=10,decimal_places=2)

    is_available = models.BooleanField(default=False)
    isTrending = models.BooleanField(default=False)

    hav_dough = models.BooleanField(default=False)
    hav_milk = models.BooleanField(default=False)
    hav_redegg = models.BooleanField(default=False)
    hav_whiteegg = models.BooleanField(default=False)
    hav_butter = models.BooleanField(default=False)
    hav_bakpow = models.BooleanField(default=False)
    hav_vanilla = models.BooleanField(default=False)
    hav_nut = models.BooleanField(default=False)

    image=models.ImageField(upload_to="products",blank=True)

    def get_price(self, size):
        size = int(size)
        if size == 1:
            return self.one_pound_price
        elif size == 2:
            return self.two_pound_price
        elif size == 3:
            return self.three_pound_price
        return 0
    

