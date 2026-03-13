
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def update_stock_and_sold(sender, instance, created, **kwargs):
    if instance.complete:

        order_items = instance.orderitem_set.all()
        for item in order_items:
            product = item.product
            if product:
                product.sold += item.quantity
                product.save()