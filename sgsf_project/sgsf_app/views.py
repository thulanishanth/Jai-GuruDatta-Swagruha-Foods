from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MenuItem

# -------------------------
# MENU PAGE
# -------------------------
@login_required
def menu(request):
    # 1. Fetch all items from DB
    items = MenuItem.objects.all()
    
    # 2. Calculate Cart Count directly here (No separate file needed)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    
    # 3. Send items AND cart_count to the template
    return render(request, "sgsf_app/menu.html", {
        "items": items,
        "cart_count": cart_count
    })


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
    
    # Calculate new total count
    new_count = sum(cart.values())
    
    # Return JSON so JavaScript can update the badge without reloading
    return JsonResponse({'status': 'success', 'cart_count': new_count})


# -------------------------
# VIEW CART PAGE
# -------------------------
@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    cart_count = sum(cart.values()) # Calculate count here too

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

# -------------------------
# BASIC PAGES
# -------------------------
def index(request):
    return render(request, 'sgsf_app/index.html')

def signup_view(request):
    # (Keep your existing signup logic here if you have it)
    pass 

def login_view(request):
    # (Keep your existing login logic here)
    pass

def logout_view(request):
    # (Keep your existing logout logic here)
    pass

@login_required
def home(request):
    return render(request, 'sgsf_app/home.html')

@login_required
def about(request):
    return render(request, 'sgsf_app/about.html')

@login_required
def profile(request):
    return render(request, 'sgsf_app/profile.html', {'user': request.user})