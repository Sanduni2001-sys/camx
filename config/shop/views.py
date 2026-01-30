
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse


from .models import (
    Product,
    CartItem,
    ServiceRequest,
    RentItem,
    RentItemCart,
    Category,
    Order,
    Profile
)


def add_product(request):
    categories = Category.objects.all()  # Categories එක ගන්න
    return render(request, 'shop/add_product.html', {'categories': categories})

# Twilio WhatsApp
from twilio.rest import Client

# ================= HOME =================
def home(request):
    products = Product.objects.all()
    rent_items = RentItem.objects.all()

    rent_cart_items = []
    product_cart_items = []

    if request.user.is_authenticated:
        rent_cart_items = RentItemCart.objects.filter(user=request.user)
        product_cart_items = CartItem.objects.filter(user=request.user)

    return render(request, 'shop/home.html', {
        'products': products,
        'rent_items': rent_items,
        'rent_cart_items': rent_cart_items,
        'product_cart_items': product_cart_items
    })
# ================= SERVICE CENTER =================
def service_center(request):
    meta = {
        'title': "Professional Camera Service - CamX.lk",
        'description': "Book professional camera repair, cleaning, and maintenance services in Sri Lanka.",
        'keywords': "Camera repair Sri Lanka, DSLR service, Camera cleaning, CamX.lk"
    }

    if request.method == "POST":
        service_name = request.POST.get("service_name")
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        preferred_date = request.POST.get("preferred_date")
        message_text = request.POST.get("message")

        # ================= SAVE TO DATABASE =================
        ServiceRequest.objects.create(
            user=request.user if request.user.is_authenticated else None,
            service_name=service_name,
            full_name=full_name,
            email=email,
            phone=phone,
            preferred_date=preferred_date,
            message=message_text
        )

        # ================= SEND EMAIL =================
        email_subject = f"🔧 New Service Request - {service_name}"
        email_message = f"""
New Camera Service Request

Service       : {service_name}
Customer Name : {full_name}
Email         : {email}
Phone         : {phone}
Preferred Date: {preferred_date}

Message:
{message_text}

---------------------------------
CamX.lk Admin Panel
        """
        try:
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False
            )
        except Exception as e:
            print("Email send failed:", e)

        # ================= SEND WHATSAPP MESSAGE =================
        try:
            client = Client(
                settings.TWILIO_ACCOUNT_SID,
                settings.TWILIO_AUTH_TOKEN
            )

            whatsapp_message = (
                f"📌 *New Service Request*\n\n"
                f"Service: {service_name}\n"
                f"Name: {full_name}\n"
                f"Phone: {phone}\n"
                f"Date: {preferred_date}\n"
            )

            message = client.messages.create(
                body=whatsapp_message,
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=settings.ADMIN_WHATSAPP_NUMBER
            )

            print("WHATSAPP SENT ✅ SID:", message.sid)
        except Exception as e:
            print("WhatsApp send failed:", e)

        messages.success(
            request,
            "✅ Your service request has been submitted successfully. Our team will contact you soon."
        )
        return redirect('service_center')

    # GET request
    return render(request, 'shop/service_center.html', {'meta': meta})




# ================= SEARCH =================

def live_search(request):
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        products = Product.objects.filter(name__icontains=query)[:5]  # top 5 results
        for p in products:
            results.append({
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'image': p.image.url,
            })

    return JsonResponse({'results': results})

# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'shop/login.html', {
            'error': 'Invalid username or password'
        })
    return render(request, 'shop/login.html')


# ================= SIGNUP =================
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            return render(request, 'shop/signup.html', {
                'error': 'Username already exists'
            })
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'shop/signup.html')

def search_results(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []

    return render(request, 'shop/search_results.html', {
        'results': results,
        'query': query
    })
def search_redirect(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('home')
    return redirect(f"{request.path}?q={query}")

# ================= PRODUCT DETAIL =================

# views.py
def product_detail(request, id):  # instead of pk
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def rent_view(request):
    
    # Rental page logic
    return render(request, 'shop/rent.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')
# ================= PROFILE =================
@login_required
def profile_view(request):
    return render(request, 'shop/profile.html')

# ================= UPDATE PROFILE =================


@login_required
def update_profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # Profile එක create නැත්නම් create කරන්න
    
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        profile_image = request.FILES.get("profile_image")  # Uploaded file

        # Email check
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "This email is already taken.")
            return redirect("profile")

        # Update User fields
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update profile image
        if profile_image:
            profile.profile_image = profile_image
            profile.save()

        messages.success(request, "✅ Your profile has been updated successfully!")
        return redirect("profile")

    return redirect("profile")
# ================= ADD TO CART =================
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')


# ================= ADD TO RENT CART =================
@login_required
def add_to_rent_cart(request, rent_item_id):
    rent_item = get_object_or_404(RentItem, id=rent_item_id)
    rent_cart_item, created = RentItemCart.objects.get_or_create(
        user=request.user,
        rent_item=rent_item
    )
    if not created:
        rent_cart_item.quantity += 1
        rent_cart_item.save()
    return redirect('home')


# ================= UPDATE CART =================
@login_required
def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    elif action == "remove":
        cart_item.delete()
    return redirect('view_cart')


# ================= VIEW CART =================
@login_required
def view_cart(request):
    product_cart_items = CartItem.objects.filter(user=request.user)
    rent_cart_items = RentItemCart.objects.filter(user=request.user)

    total_products = sum(item.total_price() for item in product_cart_items)
    total_rent = sum(item.total_price() for item in rent_cart_items)
    total = total_products + total_rent

    return render(request, 'shop/cart.html', {
        'product_cart_items': product_cart_items,
        'rent_cart_items': rent_cart_items,
        'total': total
    })


# ================= RENT PAGE =================
def rent(request):
    rent_items = RentItem.objects.all()
    return render(request, 'shop/rent.html', {'rent_items': rent_items})

# ================= UPDATE RENT CART =================
@login_required
def update_rent_cart(request, rent_cart_item_id, action):
    rent_cart_item = get_object_or_404(
        RentItemCart,
        id=rent_cart_item_id,
        user=request.user
    )

    if action == "increase":
        rent_cart_item.quantity += 1
        rent_cart_item.save()

    elif action == "decrease":
        if rent_cart_item.quantity > 1:
            rent_cart_item.quantity -= 1
            rent_cart_item.save()
        else:
            rent_cart_item.delete()

    elif action == "remove":
        rent_cart_item.delete()

    return redirect('view_cart')

from django.http import JsonResponse

# ================= RENT HISTORY VIEW =================
@login_required
def order_history_view(request):
    # user එකේ orders ගන්න
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_history.html', {'orders': orders})

from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin_temp(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin already exists")

    User.objects.create_superuser(
        username="admin",
        email="admin@camx.lk",
        password="Admin@123"
    )
    return HttpResponse("Superuser created ✅")
