import qrcode
import base64
from io import BytesIO


def generate_qr_code(order):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    data = f"{order.id}|{order.payment.transaction_id}"
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_io = BytesIO()
    qr_img.save(qr_img_io, format="PNG")
    qr_img_io.seek(0)

    # Encode the QR image as Base64
    qr_base64 = base64.b64encode(qr_img_io.read()).decode("utf-8")

    # Save the Base64 string to the order
    order.qr_code_data = qr_base64
    order.save()
    return qr_base64
