from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import JsonResponse
import json

# Create your views here.
def isadmin(user):
    return user.is_superuser

def home(request):
    med = Medicines.objects.all()
    context = {'medicines':med}
    return render(request,"index.html", context)

@login_required(login_url= 'login')
@user_passes_test(isadmin)
def add_prod(request):
    if request.method == 'POST':
        name = request.POST.get('m_name')
        description =request.POST.get('m_dec')
        price = request.POST.get('m_price')
        image = request.FILES.get('m_img')

        Medicines.objects.create(
            name = name,
            description = description,
            price = price,
            image = image,
        )
        return redirect('home')

    return render(request, 'add_prod.html')

   
def update_prod(request,pk):
    dawai = get_object_or_404(Medicines, pk = pk )
    if request.method == 'POST':
        name = request.POST.get('m_name')
        description =request.POST.get('m_dec')
        price = request.POST.get('m_price')
        image = request.FILES.get('m_img')

        dawai.name = name
        dawai.description = description
        dawai.price = price
        dawai.image = image

        dawai.save()

        return redirect('home')

    context = {'dawai':dawai}
    return render(request, 'update_prod.html', context)

def delete(request, pk):  
    
    med = get_object_or_404(Medicines, pk=pk)  
   
    med.delete()

    
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) 

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/signup.html', context)

# def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, 
            complete=False
            )
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart = request.session.get('cart', {})

        for i in cart:
            product = Medicines.objects.get(id=i)
            total = product.price * cart[i]['quantity']

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            items.append({
                'product': product,
                'quantity': cart[i]['quantity'],
                'get_total': total
            })

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, 
            complete=False
        )
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart = request.session.get('cart', {})

        for i in cart:
            # Make sure i is not empty and is a valid number
            if not i or not str(i).isdigit():
                continue

            try:
                product = Medicines.objects.get(id=int(i))
                quantity = cart[i]['quantity']
                total = product.price * quantity

                order['get_cart_total'] += total
                order['get_cart_items'] += quantity
                items.append({
                    'product': product,
                    'quantity': quantity,
                    'get_total': total
                })
            except Medicines.DoesNotExist:
                continue

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)


def deletecart(request , pk):
    if request.user.is_authenticated:
        customer = request.user
        Order.objects.filter(customer= customer ).delete()

    return render(request, 'cart.html' )

# def updateItem(request):
#     data = json.loads(request.body)
#     productId = str(data['productid'])
#     action = data['action']
#     # print('Action:', action)
#     # print('Product:', productId)
#     if request.user.is_authenticated:
#         customer = request.user
#         product = Medicines.objects.get(id=productId)
    
#     order, created = Order.objects.get_or_create(
#         customer=customer, 
#         complete=False
#         )
#     orderItem, created = OrderItem.objects.get_or_create(
#         order=order, 
#         product=product
#         )
    
#     if action == 'add':
#         orderItem.quantity += 1
#     elif action == 'remove':
#         orderItem.quantity -= 1

#     orderItem.save()
    
#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     else:
#         cart = request.session.get('cart', {})

#         if action == 'add':
#             if productId in cart:
#                 cart[productId]['quantity'] += 1
#             else:
#                 cart[productId] = {'quantity': 1}

#         elif action == 'remove':
#             if productId in cart:
#                 cart[productId]['quantity'] -= 1
#                 if cart[productId]['quantity'] <= 0:
#                     del cart[productId]

#         request.session['cart'] = cart

#     return JsonResponse("Item updated", safe=False)


# # def updateItemanon(request):
#     data = json.loads(request.body)
#     productId = data['productid']
#     action = data['action']
#     print('Action:', action)
#     print('Product:', productId)
    
#     customer = "AnonymousUser"
#     product = Medicines.objects.get(id=productId)
    
#     order, created = OrderAnon.objects.get_or_create(complete=False)
#     orderItem, created = OrderItemAnon.objects.get_or_create(order=order, product=product)
    
#     if action == 'add':
#         orderItem.quantity = (orderItem.quantity + 1)
#     elif action == 'remove':
#         orderItem.quantity = (orderItem.quantity - 1)
    
#     orderItem.save()
    
#     if orderItem.quantity <= 0:
#         orderItem.delete()
    
#     return JsonResponse("item was added", safe=False)

# ===================== Chat gpt Updated Code =====================
def updateItem(request):
    data = json.loads(request.body)
    productId = str(data['productid'])
    action = data['action']

    # ======================
    # LOGIN USER
    # ======================
    if request.user.is_authenticated:
        customer = request.user
        product = Medicines.objects.get(id=productId)

        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        orderItem, created = OrderItem.objects.get_or_create(
            order=order,
            product=product
        )

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

    # ======================
    # ANONYMOUS USER
    # ======================
    else:
        cart = request.session.get('cart', {})

        if action == 'add':
            if productId in cart:
                cart[productId]['quantity'] += 1
            else:
                cart[productId] = {'quantity': 1}

        elif action == 'remove':
            if productId in cart:
                cart[productId]['quantity'] -= 1
                if cart[productId]['quantity'] <= 0:
                    del cart[productId]

        request.session['cart'] = cart

    return JsonResponse("Item updated", safe=False)

# def cart(request):
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(
#             customer=customer,
#             complete=False
#         )
#         items = order.orderitem_set.all()

#     else:
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0}
#         cart = request.session.get('cart', {})

#         for i in cart:
#             product = Medicines.objects.get(id=i)
#             total = product.price * cart[i]['quantity']

#             order['get_cart_total'] += total
#             order['get_cart_items'] += cart[i]['quantity']

#             items.append({
#                 'product': product,
#                 'quantity': cart[i]['quantity'],
#                 'get_total': total
#             })

#     return render(request, 'cart.html', 
#                   {'items': items, 'order': order})
