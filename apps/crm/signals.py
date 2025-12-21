from django.db import transaction
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order, OrderItem
from .models import Customer


@receiver(post_save, sender=Order)
def sync_customer_metrics(sender, instance: Order, created: bool, **kwargs):
    """
    Keep basic CRM metrics in sync when an order is created.
    """
    if not created:
        return

    def _update_customer():
        if not instance.phone:
            return
        customer, _ = Customer.objects.get_or_create(
            phone=instance.phone,
            defaults={"full_name": instance.full_name or instance.phone},
        )
        if instance.full_name and instance.full_name != customer.full_name:
            customer.full_name = instance.full_name
        total_spent = (
            Order.objects.filter(phone=instance.phone).aggregate(total=Sum("total_price")).get("total") or 0
        )
        orders_count = Order.objects.filter(phone=instance.phone).count()
        customer.total_spent = total_spent
        customer.orders_count = orders_count
        customer.last_order_at = instance.created_at
        customer.save(update_fields=["full_name", "total_spent", "orders_count", "last_order_at"])

    transaction.on_commit(_update_customer)
