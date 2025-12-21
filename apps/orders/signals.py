from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Order
from apps.crm.models import Customer, InventoryLog
from .services.delivery import generate_google_maps_link
from .services.telegram import send_order_created


@receiver(pre_save, sender=Order)
def set_maps_link(sender, instance: Order, **kwargs):
    """Ensure maps_link is generated server-side when coordinates are present."""
    if instance.maps_link:
        return
    if instance.latitude is not None and instance.longitude is not None:
        instance.maps_link = generate_google_maps_link(float(instance.latitude), float(instance.longitude))


@receiver(post_save, sender=Order)
def notify_new_order(sender, instance: Order, created: bool, **kwargs):
    """
    When a customer submits a new order (checkout), send it to Telegram.
    Uses transaction.on_commit so OrderItem rows are already created.
    """
    if not created:
        return
    order_id = instance.pk

    def _post_commit():
        order = Order.objects.filter(pk=order_id).prefetch_related("items__book").first()
        if not order:
            return
        if order.phone:
            customer, _ = Customer.objects.get_or_create(
                phone=order.phone,
                defaults={"full_name": order.full_name or order.phone},
            )
            if order.customer_id != customer.id:
                order.customer = customer
                order.save(update_fields=["customer"])

        for item in order.items.all():
            book = item.book
            if book and hasattr(book, "stock_quantity"):
                book.stock_quantity = (book.stock_quantity or 0) - int(item.quantity)
                book.save(update_fields=["stock_quantity"])
                InventoryLog.objects.create(
                    book=book,
                    delta=-int(item.quantity),
                    reason="sale",
                    related_order=order,
                    note="POS" if order.order_source == "pos" else "Online buyurtma",
                )

        if order.order_source == "online":
            send_order_created(order_id)

    transaction.on_commit(_post_commit)
