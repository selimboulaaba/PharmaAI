from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from home.models import UserProfile
from items.models import Cart, CartItem, Item, Order, OrderItem
from items.forms import AddToCartForm

@login_required
def add_to_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    form = AddToCartForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=form.cleaned_data['item'])
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('cart')
    else:
            items = Item.objects.all()

    return render(request, 'items/index.html', {
        'items': items,
        'form': form
        })


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'items/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
@login_required
def delete_from_cart(request, pk):
    cartItem = get_object_or_404(CartItem, pk=pk)
    cartItem.delete()

    return redirect('cart')

@login_required
def update_quantity(request, pk):
    cartItem = get_object_or_404(CartItem, pk=pk)
    new_quantity = int(request.POST.get('quantity', 1))
    cartItem.quantity = new_quantity
    cartItem.save()

    return redirect('cart')

@login_required
def order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    order = Order.objects.create(user=request.user, price=0)

    price = 0
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=item.item,
            quantity=item.quantity,
            price=item.get_total_price()
        )
        price += item.get_total_price()

    order.price = price
    order.save()

    cart.delete()
    return redirect('orders')
    
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'items/orders.html', {'orders': orders})

