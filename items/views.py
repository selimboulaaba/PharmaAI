import django
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from home.models import UserProfile
from items.models import Cart, CartItem, Category, Item, Order, OrderItem
from items.forms import AddToCartForm

from django.shortcuts import render, redirect
from .forms import ImageUploadForm
import pytesseract
from PIL import Image, ImageFilter
from textblob import TextBlob
import cv2
import numpy as np

@login_required
def store(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    form = AddToCartForm(request.POST)
    
    categories = Category.objects.all()
    
    query = request.GET.get('query', '')
    category_filter = request.GET.get('category', '')
    sort_option = request.GET.get('sort', '')

    items = Item.objects.all()
    if query:
        items = items.filter(name__icontains=query)
    if category_filter:
        items = items.filter(category__id=category_filter)
    if sort_option:
        sort_field, sort_order = sort_option.split(',')
        if sort_order == 'asc':
            items = items.order_by(sort_field)
        else:
            items = items.order_by(f'-{sort_field}')


    if request.method == 'POST':
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=form.cleaned_data['item'])
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('cart')

    return render(request, 'items/index.html', {
        'items': items,
        'form': form,
        'categories': categories,
        'query': query,
        'category_filter': category_filter,
        'sort_option': sort_option,
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
    action = request.POST.get('action')
    if action == "increase":
        cartItem.quantity += 1
    elif action == "decrease" and cartItem.quantity > 1:
        cartItem.quantity -= 1
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

def proc_txt(text):
    text = text.split('\n')
    return text

def upload_image(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image_file = request.FILES['image']
        img = Image.open(image_file)
        try:
            img.filter(ImageFilter.SHARPEN)
        except ValueError:
            print('Got an image that failed to sharpen', image_file)
            pass
        
        image = np.array(img)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        processed_text = pytesseract.image_to_string(gray_image)        
        
        processed_text  = proc_txt(processed_text )
        cart, created = Cart.objects.get_or_create(user=request.user)
        for processed_item   in processed_text :
            items = Item.objects.all()
            for product in items:
                item_name  = product.name.lower()
                processed_item  = processed_item .lower()
                            
                set1 = set(item_name)
                set2 = set(processed_item )
                jaccard_similarity = len(set1.intersection(set2)) / len(set1.union(set2))
                if (jaccard_similarity >= 0.6):
                    item = Item.objects.get(name__iexact=item_name)
                    quantity = 1
                    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
                    cart_item.quantity += quantity
                    cart_item.save()            

    return redirect('cart')
