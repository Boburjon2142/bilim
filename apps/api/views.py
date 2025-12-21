from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.catalog.models import Book, Category, Author
from apps.orders.models import Order
from apps.crm.models import Customer, Courier
from .serializers import (
    AuthorSerializer,
    BookSerializer,
    CategorySerializer,
    OrderSerializer,
    CustomerSerializer,
    CourierSerializer,
)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.select_related("author", "category").all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.prefetch_related("items__book").all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]


class CourierViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsAdminUser]
