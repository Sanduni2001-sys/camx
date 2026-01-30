from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('service-center/', views.service_center, name='service_center'),

    # Product
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Search
    path('search/', views.search_redirect, name='search_redirect'),
    path('search/results/', views.search_results, name='search_results'),
    path('live-search/', views.live_search, name='live_search'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile_view, name='update_profile'),  # ✅ add this

    # Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-rent-cart/<int:rent_item_id>/', views.add_to_rent_cart, name='add_to_rent_cart'),
    path('update-cart/<int:cart_item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('update-rent-cart/<int:rent_cart_item_id>/<str:action>/', views.update_rent_cart, name='update_rent_cart'),

    # Orders
    path('orders/', views.order_history_view, name='order_history'),
    
    # ✅ Rent page
path('rent/', views.rent, name='rent'),


path(
    "secure-create-admin-77xk/",
    views.create_superuser_once,
),
]


