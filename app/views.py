from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
from app.models import Users, Session
from requests import get
from .serializers import UsersSerializer, SessionSerializer
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
            return render(request, "page-login.html", context)
    except KeyError:
        return render(request, "page-login.html")

        status = request.GET['status']
        context = {
        "status": status,
        }

def loginError(request):
    status = request.GET['status']
    context = {
    "status": status,
    }
    return render(request, "page-login.html", context)

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
            response = redirect('/dashboard/?ses='+ses)
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
        ses = request.GET['ses']
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

def logout(request):
    ses = request.GET['ses']
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
    return render(request, "page-login.html")
