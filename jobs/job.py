from django.core import mail
from django.conf import settings
from order.models import PendingEmail

success_subject = "Thank you for your purchase. Here's the confirmation of your order."
failure_subject = "We couldn't process your order."

def send_mails():
    connection = mail.get_connection(fail_silently=False)
    pending_emails = PendingEmail.objects.all()
    for item in pending_emails:
        order = item.order
        user = order.user
        if order.is_verified:
            order_items = order.order_items.all()
            products = []
            for order_item in order_items:
                products.append(order_item.product.name)
            body = f"""Hello {user.name}

Congratulations! Your order {order.id} is confirmed.
Items ordered: {', '.join(name for name in products)}
Total amount paid: Rs.{order.amount}

Regards
Team CCS Merchandise Store"""
            email = mail.EmailMessage(success_subject, body, settings.EMAIL_HOST_USER, [user.email], connection=connection)
            connection.send_messages([email])
        else:
            body = f"""Hello {user.name}

Unfortunately the verification for your order {order.id} has failed.
You can re-order your purchase with a valid screenshot of the payment of the required amount.

Regards
Team CCS Merchandise Store"""
            email = mail.EmailMessage(failure_subject, body, settings.EMAIL_HOST_USER, [user.email], connection=connection)
            connection.send_messages([email])
        item.delete()
    connection.close()
