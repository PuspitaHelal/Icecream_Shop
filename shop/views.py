from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import IceCream, CartItem, Order, OrderItem

# Home page: ice creams, search, pagination
def home(request):
    query = request.GET.get('q')
    if query:
        icecreams_list = IceCream.objects.filter(name__icontains=query)
    else:
        icecreams_list = IceCream.objects.all()
    
    paginator = Paginator(icecreams_list, 3)  # 3 per page
    page_number = request.GET.get('page')
    icecreams = paginator.get_page(page_number)
    
    return render(request, 'shop/home.html', {'icecreams': icecreams})

# About Us page
def about(request):
    return render(request, 'shop/about.html')

# Contact Us page
def contact(request):
    return render(request, 'shop/contact.html')

# Add to cart
@login_required
def add_to_cart(request, icecream_id):
    icecream = get_object_or_404(IceCream, id=icecream_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, ice_cream=icecream)
    if cart_item.quantity < 6:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

# View Cart
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

# Place Order
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')
    
    order = Order.objects.create(user=request.user)
    for item in cart_items:
        OrderItem.objects.create(order=order, ice_cream=item.ice_cream, quantity=item.quantity)
    cart_items.delete()
    return redirect('order_history')

# Order History
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/orders.html', {'orders': orders})