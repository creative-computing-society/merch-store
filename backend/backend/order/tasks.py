from __future__ import absolute_import, unicode_literals
import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from email.mime.image import MIMEImage
import base64
import threading


logger = logging.getLogger(__name__)


def send_order_success_email(txn_id, total, items, name, qr_code, user_email):
    subject = "Thank you for your purchase. Here's the confirmation of your order."

    context = {
        "name": name,
        "qr_code": qr_code,
        "txn_id": txn_id,
        "items": items,
        "total": total,
    }
    try:
        html_content = render_to_string("dashboard/email_success_qr.html", context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            f"CCS Merch Store <{settings.EMAIL_HOST_USER}>",
            [user_email],
        )

        email.attach_alternative(html_content, "text/html")

        qr_code_data = base64.b64decode(qr_code)

        mime_img = MIMEImage(qr_code_data)
        mime_img.add_header("Content-ID", "<qr_code>")

        email.attach(mime_img)

        email.send()
        return logger.info("Order success mail sent to {user_email}")
    except Exception as e:
        logger.error(f"Error sending order success email: {e}")
        raise


def send_order_success_email_async(txn_id, total, items, name, qr_code, user_email):
    thread = threading.Thread(
        target=send_order_success_email,
        args=(txn_id, total, items, name, qr_code, user_email),
    )
    thread.start()
