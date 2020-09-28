"""tsg123 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('member_list/', views.member_list),
    path('member_edit/', views.member_edit),
    path('member_renew/', views.member_renew),
    path('member_add/', views.member_add),

    path('borrow_record/', views.borrow_record),
    path('borrow_ret/', views.borrow_ret),
    path('borrow_bor/', views.borrow_bor),
    path('borrow_edit_memo/', views.borrow_edit_memo),

    path('book_list/', views.book_list),
    path('book_add/', views.book_add),

    path('stock_list/', views.stock_list),
    path('stock_edit/', views.stock_edit),
    path('stock_update/', views.stock_update),

    path('purchase_batch/', views.purchase_batch),
    path('purchase_add/', views.purchase_add),
    path('purchase_detail/', views.purchase_detail),
    path('purchase_add2/', views.purchase_add2),
    path('purchase_update/', views.purchase_update),

    path('cart_list/', views.cart_list),
    path('cart_del/', views.cart_del),
    path('cart_submit/', views.cart_submit),

    path('order_list/', views.order_list),

    path('listen_list/', views.listen_list),
    path('listen_update/', views.listen_update),
    path('listen_add/', views.listen_add),

    path('print_ticket/', views.print_ticket),
]
