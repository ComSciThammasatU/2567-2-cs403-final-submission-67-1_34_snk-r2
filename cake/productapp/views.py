from django.shortcuts import render, redirect, get_object_or_404
from productapp.models import Product
from commentapp.models import Comment

# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_dashboard')

    product = Product.objects.filter(isTrending=True ,is_available=True)[:3]
    return render(request, "index.html",{"product":product})

def show_products(request):
    product_list = Product.objects.filter(is_available=True)
    return render(request, 'product_list.html', {'product_list': product_list})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    allergen_mapping = {
        "แป้งสาลี": product.hav_dough,
        "นม": product.hav_milk,
        "ไข่แดง": product.hav_redegg,
        "ไข่ขาว": product.hav_whiteegg,
        "เนย": product.hav_butter,
        "ผงฟู": product.hav_bakpow,
        "วนิลลา": product.hav_vanilla,
        "ถั่ว": product.hav_nut,
    }

    comments = Comment.objects.filter(product=product).order_by('-created_at')

    return render(request, "product_detail.html", {
        "product": product,
        "allergens": [name for name, value in allergen_mapping.items() if value],
        "comments": comments 
    })

