from __future__ import absolute_import, unicode_literals
import logging
import threading


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


def send_order_completion_email(txn_id, user_name, total, items, user_email):
    subject = "Your order has been delivered successfully."

    context = {"name": user_name, "txn_id": txn_id, "items": items, "total": total}
    try:
        html_message = render_to_string("dashboard/email_delivered.html", context)
        msg = strip_tags(html_message)
        send_mail(
            subject,
            msg,
            f"CCS Merch Store <{settings.EMAIL_HOST_USER}>",
            (user_email,),
            html_message=html_message,
            fail_silently=False,
        )
        return logger.info("Order delivery confirmation mail sent to {user_email}")
    except Exception as e:
        logger.error(f"Error sending order delivery confirmation email: {e}")
        raise


def send_order_completion_email_async(txn_id, user_name, total, items, user_email):
    thread = threading.Thread(
        target=send_order_completion_email,
        args=(txn_id, user_name, total, items, user_email),
    )
    thread.start()
