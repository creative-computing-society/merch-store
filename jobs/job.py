from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
            context = {
                'name': user.name,
                'id': order.id,
                'items': ', '.join(name for name in products),
                'amount': order.amount
            }
            html_message = render_to_string('dashboard/email_order_success.html', context)
            msg = strip_tags(html_message)
            email = mail.EmailMultiAlternatives(success_subject, msg, settings.EMAIL_HOST_USER, (user.email,), connection=connection, reply_to=('ccs@thapar.edu',))
            email.attach_alternative(html_message, 'text/html')
            connection.send_messages((email,))
        else:
            context = {
                'name': user.name,
                'id': order.id
            }
            html_message = render_to_string('dashboard/email_order_failed.html')
            msg = strip_tags(html_message)
            email = mail.EmailMultiAlternatives(failure_subject, msg, settings.EMAIL_HOST_USER, (user.email,), connection=connection, reply_to=('ccs@thapar.edu',))
            email.attach_alternative(html_message, 'text/html')
            connection.send_messages((email,))
        item.delete()
    connection.close()
