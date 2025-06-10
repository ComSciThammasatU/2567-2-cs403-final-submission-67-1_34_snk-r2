from django.shortcuts import render, redirect, get_object_or_404, reverse
from productapp.models import Product
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Cart, CartItem, Order, OrderItem
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
import pandas as pd
from django.http import JsonResponse
# Create your views here.

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        size = int(request.POST.get('size'))
        quantity = int(request.POST.get('quantity', 1))
        message = request.POST.get('message', '')

        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)

        #เทสตระกร้า
        #if created:
            #print("สร้างตะกร้าใหม่ ")
        #else:   
            #print("มีตะกร้าอยู่แล้ว")

        CartItem.objects.create(
            cart=cart,
            product=product,
            size=size,
            quantity=quantity,
            message=message
        )

        return redirect('cart')  

   
    return redirect('product_detail', product_id)

@login_required   
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_items = CartItem.objects.filter(cart=cart)

    total_price = 0
    for item in cart_items:
        total_price += item.product.get_price(item.size) * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'cart_total': total_price,
    })

@login_required
def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if cart_item.cart.user == request.user:
        cart_item.delete()  
    return redirect('cart') 

@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if cart:
        cart.cartitem_set.all().delete()

    return redirect('cart') 

@login_required
def confirm_order(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart') 

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        delivery_date = request.POST.get('delivery_date')
        delivery_time = request.POST.get('delivery_time')
        address = request.POST.get('address')
        addressname = request.POST.get('addressname')
        slip = request.FILES.get('slip')

        # รวมราคาทั้งหมด
        total_price = sum(item.total_price for item in cart_items)

        # สร้าง order
        order = Order.objects.create(
            user=user,
            delivery_method=delivery_method,
            delivery_date=delivery_date,
            delivery_time=delivery_time,
            address=address,
            addressname=addressname,
            slip=slip,
            total_price=total_price,
            status='pending'
        )

        # สร้างรายการของใน order ทีละรายการ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                size=item.size,
                message=item.message,
                unit_price=item.product.get_price(item.size)
            )

        # ล้างตะกร้าหลังบันทึก
        cart_items.delete()

        return redirect('/cart/?success=true')  # ไปหน้าคำสั่งซื้อสำเร็จ

    return redirect('cart')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def manage_orders(request):
    if request.method == "POST":
        update_order_status(request)
        return redirect(request.get_full_path())  # กลับมาหน้าเดิมหลัง post

    status = request.GET.get("status", "pending")  
    orders = Order.objects.filter(status=status).order_by('created_at')
    return render(request, "manage_orders.html", {
        'orders': orders,
        'status_tab': status
    })

@login_required
@user_passes_test(is_superuser)
def update_order_status(request):
    order_id = request.POST.get("order_id")
    action = request.POST.get("action")
    order = get_object_or_404(Order, id=order_id)

    if action == "cancel_order":
        cancel_reason = request.POST.get("cancel_reason", "")
        order.status = "cancelled"
        order.cancel_reason = cancel_reason
        order.save()
    

        return redirect(reverse('manage_orders') + '?status=pending')

    if action == "confirm_payment":
        order.status = "paid"
    elif action == "confirm_shipping":
        order.status = "shipped"
    order.save()

@login_required
@user_passes_test(is_superuser)
def sales_dashboard(request):
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    total_today = Order.objects.filter(status='shipped', created_at__date=today).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    total_yesterday = Order.objects.filter(status='shipped', created_at__date=yesterday).aggregate(
        total=Sum('total_price')
    )['total'] or 0

    total_month = Order.objects.filter(
        status='shipped',
        created_at__year=today.year,
        created_at__month=today.month
    ).aggregate(total=Sum('total_price'))['total'] or 0

    return render(request, 'sales_sum.html', {
        'total_today': total_today,
        'total_yesterday': total_yesterday,
        'total_month': total_month
    })

@login_required
@user_passes_test(is_superuser)
def sales_sum(request):
    orders = Order.objects.filter(status='shipped').values('total_price', 'delivery_date')

    if not orders:
        return JsonResponse({}, status=204)

    df = pd.DataFrame.from_records(orders)

    df['delivery_date'] = pd.to_datetime(df['delivery_date'])

    df['year'] = df['delivery_date'].dt.year
    df['month'] = df['delivery_date'].dt.month

    grouped = df.groupby(['year', 'month'])['total_price'].sum().unstack(fill_value=0)

    result = {}
    for year in grouped.index:
        monthly_data = [float(grouped.loc[year].get(m, 0)) for m in range(1, 13)]
        result[str(year)] = monthly_data

    return JsonResponse(result)
