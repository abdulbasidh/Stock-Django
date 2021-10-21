from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from app.models import Users, Session, Products, Supplier
from requests import get
from .serializers import UsersSerializer, SessionSerializer, ProductsSerializer, SupplierSerializer
import hashlib
import string
import random

def login(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).filter(status="active").exists():
            response = redirect('/dashboard/?ses='+ses)
            return response
        else:
            return render(request, "login.html", context)
    except KeyError:
        return render(request, "login.html")

        status = request.GET['status']
        context = {
        "status": status,
        }

def loginError(request):
    status = request.GET['status']
    context = {
    "status": status,
    }
    return render(request, "login.html", context)

def LoginAction(request):
    ip = get('https://api.ipify.org').text
    email = request.POST.get('email', False);
    password = request.POST.get('password', False);

    password_gen = hashlib.sha256(password.encode())
    encryppass=password_gen.hexdigest()

    rawtoken=''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
    token_gen = hashlib.sha256(rawtoken.encode())
    ses=token_gen.hexdigest()
    if Users.objects.filter(email=email).exists():
        if Users.objects.filter(password=encryppass).exists():
            data = {
                'email': email,
                'token': ses,
                'status': 'active',
                'ip': ip,
            }
            serializer = SessionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            response = redirect('/dashboard/')
            response.set_cookie('ses', ses)
            return response
        else:
            status="email or password does not match"
            response = redirect('/loginError/?status='+status)
            print(email)
            return response
    else:
        status="email or password does not match"
        response = redirect('/loginError/?status='+status)
        print(email)
        return response

def DashboardView(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                data1 = Session.objects.get(token=ses)
                email = data1.email
                data2 = Users.objects.get(email=email)
                username = data2.username
                context = {
                "ses": ses,
                "email": email,
                "username": username,
                }
                return render(request, "dashboard.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "dashboard.html", context)

def ProductsView(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                products = Products.objects.all()
                context= {'products': products}
                return render(request, "products.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "dashboard.html", context)

def addProducts(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                data1 = Session.objects.get(token=ses)
                email = data1.email
                data2 = Users.objects.get(email=email)
                username = data2.username
                context = {
                "ses": ses,
                "email": email,
                "username": username,
                }
                return render(request, "add-products.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "add-products.html", context)

def addProductsAction(request):
    ses  = request.COOKIES['ses']
    prodid = ''.join(random.sample('0123456789', 5))
    prodname = request.POST.get('prodname', False);
    prodqty = request.POST.get('prodqty', False);
    prodprice = request.POST.get('prodprice', False);
    prodseller = request.POST.get('prodseller', False);

    # Saving in DB
    products = Products(product_id=prodid,prod_name=prodname,qty=prodqty,tot_price=prodprice,seller=prodseller)
    products.save()

    status="Product Added Successfully"
    response = redirect('/prodConfirm/?ses='+ses+'&status='+status)
    print(prodid, prodname, prodqty, prodprice, prodseller)
    return response
    return render(request, "add-products.html", context)

def prodConfirm(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                status = request.GET['status']
                context = {
                "status": status,
                "ses": ses,
                }
                return render(request, "add-products.html", context)
            else:
                response = redirect('/add-products/')
                return response
        else:
            response = redirect('/add-products/')
            return response
    except KeyError:
        response = redirect('/add-products/')
        return response
    return render(request, "add-products.html", context)

def show(request):
        '''
        List all the todo items for given requested user
        '''
        """
        products = Products.objects.all()
        serializer = ProductsSerializer(products, many=True)
        serializerjson = json.dumps(serializer.data)
        serializerjson = context
        """

        products = Products.objects.all()
        context= {'products': products}

        return render(request, "file.html", context)

def prodEdit(request):
    try:
        ses = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                id = request.GET['id']
                products = Products.objects.all()
                context = {
                "products": products,
                "ses": ses,
                }

                return render(request, "edit-products.html", context)
            else:
                response = redirect('/products/')
                return response
        else:
            response = redirect('/products/')
            return response
    except KeyError:
        response = redirect('/products/')
        return response
    return render(request, "edit-products.html", context)

def prodDelete(request):
    try:
        ses = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                id = request.GET['id']
                products = Products.objects.all()
                Products.objects.filter(product_id=id).delete()
                context = {
                "status": "Product deleted successfully!",
                "products": products,
                "ses": ses,
                "id": id,
                }
                return render(request, "products.html", context)
            else:
                response = redirect('/products/')
                return response
        else:
            response = redirect('/products/')
            return response
    except KeyError:
        response = redirect('/products/')
        return response
    return render(request, "products.html", context)

def editProductsAction(request):
    ses  = request.COOKIES['ses']
    prodid = request.POST.get('prodid', False);
    prodname = request.POST.get('prodname', False);
    prodqty = request.POST.get('qty', False);
    prodprice = request.POST.get('price', False);
    prodseller = request.POST.get('seller', False);

    Products.objects.filter(product_id=prodid).update(prod_name=prodname,qty=prodqty,tot_price=prodprice,seller=prodseller)

    print(prodid)
    products = Products.objects.all()
    context = {
    "statusupdated": "Product updated successfully!",
    "products": products,
    }
    return render(request, "products.html", context)
    print(prodid, prodname, prodqty, prodprice, prodseller)
    return response
    return render(request, "add-products.html", context)

def supplierView(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                supplier = Supplier.objects.all()
                context= {'supplier': supplier}
                return render(request, "sellers.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "sellers.html", context)

def addSupplier(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                data1 = Session.objects.get(token=ses)
                email = data1.email
                data2 = Users.objects.get(email=email)
                username = data2.username
                context = {
                "ses": ses,
                "email": email,
                "username": username,
                }
                return render(request, "add-sellers.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "add-sellers.html", context)

def addSupplierAction(request):
    ses  = request.COOKIES['ses']
    supid = ''.join(random.sample('0123456789', 5))
    supname = request.POST.get('seller-name', False);
    supphn = request.POST.get('seller-phone', False);
    supaddrs = request.POST.get('seller-address', False);

    # Saving in DB
    seller = Supplier(supplier_id=supid,sup_name=supname,address=supaddrs,phone=supphn)
    seller.save()

    status="Supplier Added Successfully"
    response = redirect('/supplierConfirm/?status='+status)
    return response
    return render(request, "add-products.html", context)

def supplierConfirm(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                status = request.GET['status']
                context = {
                "status": status,
                "ses": ses,
                }
                return render(request, "add-sellers.html", context)
            else:
                response = redirect('/addSupplier/')
                return response
        else:
            response = redirect('/addSupplier/')
            return response
    except KeyError:
        response = redirect('/addSupplier/')
        return response
    return render(request, "add-sellers.html", context)

def supplierDelete(request):
    try:
        ses = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                id = request.GET['id']
                supplier = Supplier.objects.all()
                Supplier.objects.filter(supplier_id=id).delete()
                context = {
                "status": "Supplier deleted successfully!",
                "supplier": supplier,
                "ses": ses,
                "id": id,
                }
                return render(request, "sellers.html", context)
            else:
                response = redirect('/seller/')
                return response
        else:
            response = redirect('/seller/')
            return response
    except KeyError:
        response = redirect('/seller/')
        return response
    return render(request, "sellers.html", context)

def supplierEdit(request):
    try:
        ses = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                id = request.GET['id']
                supplier = Supplier.objects.filter(supplier_id=id)
                context = {
                "supplier": supplier,
                "ses": ses,
                }
                return render(request, "edit-sellers.html", context)
            else:
                response = redirect('/seller/')
                return response
        else:
            response = redirect('/seller/')
            return response
    except KeyError:
        response = redirect('/seller/')
        return response
    return render(request, "edit-sellers.html", context)

def editSupplierAction(request):
    ses  = request.COOKIES['ses']
    supid = request.POST.get('seller-id', False);
    supname = request.POST.get('seller-name', False);
    supphn = request.POST.get('seller-phone', False);
    supaddrss = request.POST.get('seller-address', False);

    Supplier.objects.filter(supplier_id=supid).update(sup_name=supname,address=supaddrss,phone=supphn)

    print(supid)
    supplier = Supplier.objects.all()
    context = {
    "statusupdated": "Supplier updated successfully!",
    "supplier": supplier,
    }
    return render(request, "sellers.html", context)
    return response
    return render(request, "add-sellers.html", context)

def settingsView(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                user = Users.objects.all()
                context= {'user': user}
                return render(request, "settings.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "settings.html", context)

def settingsAction(request):
    ses  = request.COOKIES['ses']
    id = request.POST.get('id', False);
    username = request.POST.get('username', False);
    email = request.POST.get('email', False);

    Users.objects.filter(id=id).update(id=id,username=username,email=email)

    status="Updated Successfully"
    response = redirect('/settingsConfirm/?status='+status)
    return response
    return render(request, "settings.html", context)

def settingsConfirm(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                status = request.GET['status']
                user = Users.objects.all()
                context = {
                "status": status,
                "ses": ses,
                "user": user,
                }
                return render(request, "settings.html", context)
            else:
                response = redirect('/settings/')
                return response
        else:
            response = redirect('/settings/')
            return response
    except KeyError:
        response = redirect('/settings/')
        return response
    return render(request, "settings.html", context)

def cpassView(request):
    try:
        ses  = request.COOKIES['ses']
        if Session.objects.filter(token=ses).exists():
            if Session.objects.filter(status="active").exists():
                user = Users.objects.all()
                context= {'user': user}
                return render(request, "change-password.html", context)
            else:
                response = redirect('/login/')
                return response
        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "change-password.html", context)

def cpassAction(request):
    ses  = request.COOKIES['ses']
    id = request.POST.get('id', False);
    password = request.POST.get('password', False);

    password_gen = hashlib.sha256(password.encode())
    encryppass=password_gen.hexdigest()

    Users.objects.filter(id=id).update(password=encryppass)

    status="Password updated successfully!"
    response = redirect('/settingsConfirm/?status='+status)
    return response
    return render(request, "settings.html", context)

def logout(request):
    ses  = request.COOKIES['ses']
    try:
        if Session.objects.filter(token=ses).filter(status="active").exists():
            Session.objects.filter(token=ses).update(status="inactive")
            response = redirect('/login/')
            response.delete_cookie('ses')
            return response

        else:
            response = redirect('/login/')
            return response
    except KeyError:
        response = redirect('/login/')
        return response
    return render(request, "login.html")
