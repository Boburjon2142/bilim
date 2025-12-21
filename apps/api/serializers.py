from rest_framework import serializers

from apps.catalog.models import Book, Category, Author
from apps.orders.models import Order, OrderItem
from apps.crm.models import Customer, Courier


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio", "is_featured"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent_id"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "author",
            "sale_price",
            "barcode",
            "stock_quantity",
            "created_at",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "full_name",
            "phone",
            "status",
            "order_source",
            "total_price",
            "created_at",
            "items",
        ]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "full_name", "phone", "discount_percent", "total_spent", "orders_count"]


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ["id", "name", "phone", "telegram_username", "is_active"]
