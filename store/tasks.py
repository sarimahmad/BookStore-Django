from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from .models import Purchase
from django.conf import settings


@shared_task
def send_purchase_email(purchase_id):
    print(purchase_id)
    subject = 'Purchase Confirmation'
    message, user_email = PurchaseItemData(purchase_id)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
    return None


def PurchaseItemData(purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    user_email = purchase.user.email
    message = f'Thank you for your purchase!\n\nPurchase ID: {purchase.id}\nTotal Amount: {purchase.total_amount}\n\nBooks:\n'
    for item in purchase.purchase_items.all():
        message += f'{item.book.title} - {item.quantity} x ${item.price}\n'

    return message, user_email
