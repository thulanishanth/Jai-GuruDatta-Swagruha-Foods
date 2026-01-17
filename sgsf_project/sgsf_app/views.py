from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import MenuItem, OrderItem
from .forms import CheckoutForm
# -------------------------
# AUTHENTICATION VIEWS
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
    print("DEBUG: Items in DB:", items.count())
    return render(request, "sgsf_app/menu.html", {"items": items})


@login_required
def about(request):
    return render(request, 'sgsf_app/about.html')



@login_required
def profile(request):
    # Pass the logged-in user object to template
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