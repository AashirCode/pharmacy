from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
import json

# Create your views here.
def home(request):
    med = Medicines.objects.all()
    context = {'medicines':med}
    return render(request,"index.html", context)

    
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
#     if request.user.is_authenticated:
#         customer = request.user
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#     else:
#         items = []
#         order = {'get_cart_total': 0, 'get_cart_items': 0}

#     context = {'items': items, 'order': order}
#     return render(request, 'cart.html', context)

def cart(request):
    customer = request.user
    if customer:
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order, created = Order.objects.get_or_create(customer="null", complete=False)
    
    items = order.orderitem_set.all()

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productid']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user
    product = Medicines.objects.get(id=productId)
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("item was added", safe=False)
