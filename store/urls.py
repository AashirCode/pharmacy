"""
URL configuration for pharmacy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from . import views

from pharmacy import settings

urlpatterns = [
    path('register/', views.register, name='register'),

    path('', views.home, name='home'),
    path('add_product/', views.add_prod, name='add_product'),
    path('update_prod/<pk>', views.update_prod, name='update_prod'),
    path('delete/<pk>', views.delete, name='delete'),
    path('cart/', views.cart, name='cart'),    
    path('update_item/', views.updateItem, name='update_item'),
    path('update_item_anon/', views.updateItemanon, name='update_item_anon'),
]

