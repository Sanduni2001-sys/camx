from .models import RentItemCart, CartItem

def cart_context(request):
    if request.user.is_authenticated:
        rent_cart_items = RentItemCart.objects.filter(user=request.user)
        product_cart_items = CartItem.objects.filter(user=request.user)
    else:
        rent_cart_items = []
        product_cart_items = []
    return {
        'rent_cart_items': rent_cart_items,
        'product_cart_items': product_cart_items
    }