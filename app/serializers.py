from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Users, Session, Products

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["email","username","password"]

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["email","token","status","ip"]

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["product_id","prod_name","qty","tot_price","seller"]
