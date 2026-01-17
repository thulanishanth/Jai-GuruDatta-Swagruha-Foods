from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CheckoutForm, SignupForm
from .models import MenuItem, OrderItem

# -------------------------
# INDEX / AUTHENTICATION
# -------------------------
def index(request):
    return render(request, 'sgsf_app/index.html')


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'sgsf_app/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'sgsf_app/login.html', {'error': 'Invalid Credentials'})

    return render(request, 'sgsf_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


# -------------------------
# MAIN PAGES
# -------------------------
@login_required
def home(request):
    return render(request, 'sgsf_app/home.html')


@login_required
def menu(request):
    items = MenuItem.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, "sgsf_app/menu.html", {"items": items, "cart_count": cart_count})


# -------------------------
# AJAX ADD TO CART (No Refresh)
# -------------------------
def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1
    else:
        cart[item_id] = 1

    request.session['cart'] = cart

    new_count = sum(cart.values())
    return JsonResponse({'status': 'success', 'cart_count': new_count})


# -------------------------
# VIEW CART PAGE
# -------------------------
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    cart_count = sum(cart.values())

    for item_id, qty in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            total_price = menu_item.price * qty
            grand_total += total_price

            cart_items.append({
                'id': menu_item.id,
                'name': menu_item.name,
                'price': menu_item.price,
                'image': menu_item.image,
                'qty': qty,
                'total': total_price
            })
        except MenuItem.DoesNotExist:
            continue

    return render(request, 'sgsf_app/cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'cart_count': cart_count
    })


# -------------------------
# CART ACTIONS (+ / - / Remove)
# -------------------------
def increase_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        cart[item_id] += 1
        request.session['cart'] = cart

    return redirect('view_cart')


def decrease_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        if cart[item_id] > 1:
            cart[item_id] -= 1
        else:
            del cart[item_id]

        request.session['cart'] = cart

    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id = str(item_id)

    if item_id in cart:
        del cart[item_id]
        request.session['cart'] = cart

    return redirect('view_cart')


@login_required
def about(request):
    return render(request, 'sgsf_app/about.html')


@login_required
def profile(request):
    return render(request, 'sgsf_app/profile.html', {'user': request.user})

#-------------------------
# CHECKOUT VIEW
#-------------------------

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('menu')
    
    
    grand_total = 0
    for item_id, item_details in cart.items():
        item = MenuItem.objects.get(id=item_id)
        grand_total += item.price * item_details['quantity']
        
    
    if request.method == 'POST':
        form = CheckoutForm(request.Post)
        if form.is_valid():
            
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = grand_total
            order.save()
            
            for item_id, item_details in cart.items():
                item = MenuItem.objects.get(id=item_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=item,
                    price=item.price,
                    quantity=item_details['quantity']
                )

            del request.session['cart']
            
            return redirect('order_success')
        else:
            form = CheckoutForm()
        
        return render(request, 'sgsf_app/checkout.html', {
            'form': form,
            'grand_total': grand_total
        })
        
@login_required
def order_success(request):
    return render(request, 'sgsf_app/order_success.html')