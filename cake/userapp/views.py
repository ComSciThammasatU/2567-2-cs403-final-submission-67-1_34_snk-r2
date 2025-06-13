from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from productapp.models import Product
from commentapp.models import Comment
from productapp.forms import ProductForm
from django.http import HttpResponseRedirect
from requests.auth import HTTPBasicAuth
from django.contrib import messages
import random
import requests
import base64
from django.conf import settings
from django.http import JsonResponse
# Create your views here.

User = get_user_model()

"""
def user_login(request):
    error = None
    if request.method == "POST":
        phone = request.POST["phone"]
        password = request.POST["password"]
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            error = "เบอร์โทรศัพท์หรือรหัสผ่านไม่ถูกต้อง"
    return render(request, "login.html", {"error": error})

def register(request):
    error = None
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = request.POST["phone"]
        password = request.POST["password"]
        confirm = request.POST["confirm_password"]
        if User.objects.filter(phone=phone).exists():
            error = "เบอร์นี้มีผู้ใช้งานแล้ว"
        elif password != confirm:
            error = "รหัสผ่านไม่ตรงกัน"
        else:
            User.objects.create_user(
                phone=phone,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return redirect("login")
    return render(request, "register.html", {"error": error})
"""

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    product = Product.objects.filter(isTrending=True ,is_available=True)
    return render(request, "admin_dashboard.html",{"product":product})

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
@user_passes_test(is_superuser)
def edit_menu(request):
    products = Product.objects.all()
    return render(request, 'edit.html', {'products': products})
'''''
@login_required
@user_passes_test(is_superuser)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('edit_menu')
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_form.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('edit_menu') 
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
'''

@login_required
@user_passes_test(is_superuser)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        one_pound_price = request.POST.get('price1')
        two_pound_price = request.POST.get('price2')
        three_pound_price = request.POST.get('price3')
        isTrending = 'isTrending' in request.POST

        hav_dough = 'havDough' in request.POST
        hav_milk = 'havMilk' in request.POST
        hav_redegg = 'havRedegg' in request.POST
        hav_whiteegg = 'havWhiteegg' in request.POST
        hav_butter = 'havButter' in request.POST
        hav_bakpow = 'havBakpow' in request.POST
        hav_vanilla = 'havVanilla' in request.POST
        hav_nut = 'havNut' in request.POST

        image = request.FILES.get('imageUpload')

        Product.objects.create(
            name=name,
            description=description,
            one_pound_price=one_pound_price,
            two_pound_price=two_pound_price,
            three_pound_price=three_pound_price,
            isTrending=isTrending,
            hav_dough=hav_dough,
            hav_milk=hav_milk,
            hav_redegg=hav_redegg,
            hav_whiteegg=hav_whiteegg,
            hav_butter=hav_butter,
            hav_bakpow=hav_bakpow,
            hav_vanilla=hav_vanilla,
            hav_nut=hav_nut,
            image=image
        )
        return redirect('edit_menu')

    return render(request, 'addmenu2.html')

@login_required
@user_passes_test(is_superuser)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.one_pound_price = request.POST.get('price1')
        product.two_pound_price = request.POST.get('price2')
        product.three_pound_price = request.POST.get('price3')
        product.isTrending = 'isTrending' in request.POST

        product.hav_dough = 'havDough' in request.POST
        product.hav_milk = 'havMilk' in request.POST
        product.hav_redegg = 'havRedegg' in request.POST
        product.hav_whiteegg = 'havWhiteegg' in request.POST
        product.hav_butter = 'havButter' in request.POST
        product.hav_bakpow = 'havBakpow' in request.POST
        product.hav_vanilla = 'havVanilla' in request.POST
        product.hav_nut = 'havNut' in request.POST

        if request.FILES.get('imageUpload'):
            product.image = request.FILES['imageUpload']

        product.save()

        return redirect('edit_menu')

    return render(request, 'editmenu2.html', {'product': product})


@login_required
@user_passes_test(is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('edit_menu')

@login_required
@user_passes_test(is_superuser)
def toggle_available(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_available = not product.is_available
    product.save()
    return redirect("edit_menu")


def user_login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = authenticate(request, phone=phone, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True})

        return JsonResponse({"success": False, "error": "เบอร์โทรศัพท์หรือรหัสผ่านไม่ถูกต้อง"})

    return JsonResponse({"success": False, "error": "ไม่สามารถประมวลผลคำขอได้"})


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if User.objects.filter(phone=phone).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': "เบอร์นี้มีผู้ใช้งานแล้ว"})
            else:
                messages.error(request, "เบอร์นี้มีผู้ใช้งานแล้ว")
                return redirect('home')

        if password != confirm_password:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': "รหัสผ่านไม่ตรงกัน"})
            else:
                messages.error(request, "รหัสผ่านไม่ตรงกัน")
                return redirect('home')

        otp_code = send_otp(phone)
        if otp_code:
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['phone'] = phone
            request.session['password'] = password
            request.session['otp_code'] = otp_code
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            else:
                return redirect('verify_otp')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': "ส่ง OTP ไม่สำเร็จ"})
            else:
                messages.error(request, "ส่ง OTP ไม่สำเร็จ")
                return redirect('home')

    return redirect('home')


def send_otp(phone):
   
    #เทส
    #if settings.DEBUG:
        #otp_code = "111111"
        #print(f"OTP สำหรับ {phone} คือ {otp_code}")  
        #return otp_code
    #else:
    
    if phone.startswith('0'):
        phone = '66' + phone[1:]

    otp_code = str(random.randint(100000, 999999))

    #print(f"OTP สำหรับ {phone} คือ {otp_code}")

    url = "https://api-v2.thaibulksms.com/sms"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "msisdn": phone,
        "message": f"รหัส OTP ของคุณคือ {otp_code}",
        "sender": "ProjectOTP" 
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        auth=HTTPBasicAuth(settings.THAIBULKSMS_API_KEY, settings.THAIBULKSMS_API_SECRET)
    )

    try:
        result = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        return None

    print("DEBUG result =", result)

    return otp_code


def verify_otp(request):
    if request.method == "POST":
        input_otp = request.POST.get("otp")
        session_otp = request.session.get('otp_code')

        if input_otp == session_otp:
            first_name = request.session.get('first_name')
            last_name = request.session.get('last_name')
            phone = request.session.get('phone')
            password = request.session.get('password')

            user = User.objects.create_user(
                phone=phone,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            login(request, user)

         
            for key in ['first_name', 'last_name', 'phone', 'password', 'otp_code']:
                if key in request.session:
                    del request.session[key]

            return JsonResponse({"success": True})

        else:
            return JsonResponse({"success": False, "error": "OTP ไม่ถูกต้อง"})  

    return JsonResponse({"success": False, "error": "ไม่สามารถประมวลผลคำขอได้"})

