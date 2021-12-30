from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import OrderSerializer
from .models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
