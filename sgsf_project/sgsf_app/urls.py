from django.urls import path
from . import views

urlpatterns = [
    # -------------------------
    # AUTHENTICATION
    # -------------------------
    path('', views.index, name='index'),              # Landing page
    path('signup/', views.signup_view, name='signup'),# Signup page
    path('login/', views.login_view, name='login'),   # Login page
    path('logout/', views.logout_view, name='logout'),# Logout function

    # -------------------------
    # MAIN PAGES
    # -------------------------
    path('home/', views.home, name='home'),           # Home page
    path('menu/', views.menu, name='menu'),           # Menu page

    # -------------------------
    # NAVBAR LINKS
    # -------------------------
    path('about/', views.about, name='about'),        # About pages
    path('profile/', views.profile, name='profile'),  # Profile page (shows logged-in user)
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-cart/<int:item_id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:item_id>/', views.decrease_cart, name='decrease_cart'),
]
