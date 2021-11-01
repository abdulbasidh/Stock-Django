"""stockmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include, url
from app.views import login, LoginAction, DashboardView, logout, loginError, ProductsView, addProducts, addProductsAction, prodConfirm, prodDelete, prodEdit, editProductsAction, supplierView, addSupplier, addSupplierAction, supplierConfirm, supplierDelete, supplierEdit, editSupplierAction, settingsView, settingsAction, settingsConfirm, cpassView, cpassAction, show, shop, buy, buyaction, fpassword, fpassAction, fpassOtp, fpassOtpAction

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^LoginAction/$', LoginAction, name='LoginAction'),
    url(r'^login/$', login, name='login'),
    url(r'^loginError/$', loginError, name='loginError'),
    url(r'^logout/$', logout, name='Logout'),
    path('dashboard/', DashboardView, name="Dashboard"),
    path('products/', ProductsView, name="Products"),
    path('add-products/', addProducts, name="addProducts"),
    path('add-products-action/', addProductsAction, name="addProductsAction"),
    path('prodConfirm/', prodConfirm, name="prodConfirm"),
    path('prodEdit/', prodEdit, name="prodEdit"),
    path('editProductsAction/', editProductsAction, name="editProductsAction"),
    path('prodDelete/', prodDelete, name="prodDelete"),

    path('seller/', supplierView, name="Seller"),
    path('addSupplier/', addSupplier, name="addSellers"),
    path('addSupplierAction/', addSupplierAction, name="addSupplierAction"),
    path('supplierConfirm/', supplierConfirm, name="supplierConfirm"),
    path('supplierDelete/', supplierDelete, name="supplierDelete"),
    path('supplierEdit/', supplierEdit, name="prodEdit"),
    path('editSupplierAction/', editSupplierAction, name="editSupplierAction"),


    path('settings/', settingsView, name="Settings"),
    path('settingsAction/', settingsAction, name="settingsAction"),
    path('settingsConfirm/', settingsConfirm, name="settingsConfirm"),

    path('password/', cpassView, name="Password"),
    path('cpassAction/', cpassAction, name="cpassAction"),

    path('shop/', shop, name="shop"),
    path('buy/', buy, name="buy"),
    path('buyaction/', buyaction, name="buyaction"),

    path('fpassword/', fpassword, name="fpassword"),
    path('fpassAction/', fpassAction, name="fpassAction"),
    path('fpassOtp/', fpassOtp, name="fpassOtp"),
    path('fpassOtpAction/', fpassOtpAction, name="fpassOtpAction"),
]
