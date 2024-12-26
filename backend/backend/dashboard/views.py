from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    StreamingHttpResponse,
)
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum

from order.models import Order, OrderItem, Payment
from products.models import Product, CartItem
from login.models import CustomUser
from discounts.models import DiscountCode
from .utils import get_for_user_positions

from .tasks import send_order_completion_email_async

import csv


class ListItem:
    def __init__(self, id, name, price, orders_count):
        self.id = id
        self.name = name
        self.price = price
        self.orders_count = orders_count


# Create your views here.


@staff_member_required
def dashboard(request):
    amount_received = (
        Order.objects.filter(is_verified=True).aggregate(total=Sum("updated_amount"))[
            "total"
        ]
        or 0
    )
    unsuccessful_orders = Order.objects.filter(is_verified=False).count()
    pending_orders = Order.objects.filter(is_verified=None).count()
    items_ordered = (
        OrderItem.objects.all().aggregate(total=Sum("quantity"))["total"] or 0
    )
    # items_ordered = 0

    items = []
    products = Product.objects.all()
    for product in products:
        orders_count = OrderItem.objects.filter(
            product=product, order__is_verified=True
        ).count()
        quantity_count = (
            OrderItem.objects.filter(
                product=product, order__is_verified=True
            ).aggregate(total=Sum("quantity"))["total"]
            or 0
        )
        item = {
            "id": product.id,
            "name": product.name,
            "quantity": quantity_count,
            "price": product.price,
            "orders_count": orders_count,
        }
        items.append(item)

    users = CustomUser.objects.all()
    user_orders = {user: Order.objects.filter(user=user) for user in users}
    payments = Payment.objects.all()

    context = {
        "amount_received": amount_received,
        "items_ordered": items_ordered,
        "unsuccessful_orders": unsuccessful_orders,
        "pending_orders": pending_orders,
        "items": items,
        "productsCount": len(items),
        "user_orders": user_orders,
        "payments": payments,
    }

    return render(request, "dashboard/dashboard.html", context=context)


@staff_member_required
def discount_codes(request):
    discount_codes = DiscountCode.objects.all().order_by("-created_at")
    return render(
        request,
        "dashboard/discount_codes.html",
        {"discount_codes": discount_codes},
    )


@staff_member_required
def create_discount_code(request):
    if request.method == "POST":
        code = request.POST.get("code")
        discount_percentage = request.POST.get("discount_percentage")
        max_uses = request.POST.get("max_uses")
        expiry_date = request.POST.get("expiry_date")
        for_user_positions = request.POST.get("for_user_positions")
        custom = request.POST.get("custom", False) == "on"

        for_user_positions = get_for_user_positions(for_user_positions)

        discount_code = DiscountCode(
            code=code if custom else None,
            discount_percentage=discount_percentage,
            max_uses=max_uses,
            expiry_date=expiry_date,
            for_user_positions=for_user_positions,
            custom=custom,
        )
        discount_code.save()
        messages.success(request, "Discount code created successfully.")
        return redirect("/discount-codes")
    return render(request, "dashboard/discount_codes.html")


@staff_member_required
def edit_discount_code(request, code_id):
    discount_code = get_object_or_404(DiscountCode, id=code_id)

    if request.method == "POST":
        code = request.POST.get("code")
        discount_percentage = request.POST.get("discount_percentage")
        max_uses = request.POST.get("max_uses")
        expiry_date = request.POST.get("expiry_date")
        for_user_positions = request.POST.get("for_user_positions")
        custom = request.POST.get("custom", False) == "on"

        for_user_positions = get_for_user_positions(for_user_positions)

        discount_code.code = code
        discount_code.discount_percentage = discount_percentage
        discount_code.max_uses = max_uses
        discount_code.expiry_date = expiry_date
        discount_code.for_user_positions = for_user_positions
        discount_code.custom = custom

        discount_code.save()
        messages.success(request, "Discount code updated successfully.")
        return redirect("/discount-codes")
    return render(
        request, "dashboard/discount_codes.html", {"discount_code": discount_code}
    )


@staff_member_required
def delete_discount_code(request, code_id):
    discount_code = get_object_or_404(DiscountCode, id=code_id)
    discount_code.delete()
    messages.success(request, "Discount code deleted successfully.")
    return redirect("/discount-codes")


class Echo:
    def write(self, value):
        return value


@staff_member_required
@require_POST
def stopOrders(request):
    products = Product.objects.all()
    for product in products:
        product.accept_orders = False
        product.save()
    cart_items = CartItem.objects.all()
    for cart_item in cart_items:
        cart_item.delete()
    messages.success(request, "Stopped receiving orders and cleared all carts")
    return redirect("/dashboard")


@staff_member_required
@require_POST
def startOrders(request):
    products = Product.objects.all()
    for product in products:
        product.accept_orders = True
        product.save()
    messages.success(request, "Started receiving orders")
    return redirect("/dashboard")


@staff_member_required
def products(request):
    products = Product.objects.all()
    return render(request, "dashboard/products.html", {"products": products})


@staff_member_required
def create_product(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        max_quantity = request.POST.get("max_quantity")
        for_user_positions = request.POST.get("for_user_positions")
        is_size_required = request.POST.get("is_size_required", False) == "on"
        is_name_required = request.POST.get("is_name_required", False) == "on"
        is_image_required = request.POST.get("is_image_required", False) == "on"
        accept_orders = request.POST.get("accept_orders", False) == "on"
        description = request.POST.get("description")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        size_chart_image = request.FILES.get("size_chart_image")

        for_user_positions = get_for_user_positions(for_user_positions)

        product = Product(
            name=name,
            price=price,
            max_quantity=max_quantity,
            is_size_required=is_size_required,
            is_name_required=is_name_required,
            is_image_required=is_image_required,
            for_user_positions=for_user_positions,
            accept_orders=accept_orders,
            description=description,
            image1=image1,
            image2=image2,
            size_chart_image=size_chart_image,
        )
        product.save()
        messages.success(request, "Product created successfully.")
        return redirect("/products")
    return render(request, "dashboard/products.html")


@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.max_quantity = request.POST.get("max_quantity")
        product.for_user_positions = request.POST.get("for_user_positions")

        product.for_user_positions = get_for_user_positions(product.for_user_positions)

        product.is_size_required = request.POST.get("is_size_required", False) == "on"
        product.is_name_required = request.POST.get("is_name_required", False) == "on"
        product.is_image_required = request.POST.get("is_image_required", False) == "on"
        product.accept_orders = request.POST.get("accept_orders", False) == "on"
        product.description = request.POST.get("description")

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect("/products")
    return render(request, "dashboard/products.html")


@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("/products")


@staff_member_required
def render_qr_page(request):
    return render(request, "dashboard/scan_qr.html")


@staff_member_required
def scan_qr(request):
    if request.method == "POST":
        scanned_qr_code = request.POST.get("scanned_qr_code")
        try:
            order_id, txnid = scanned_qr_code.split("|")
            order = Order.objects.get(pk=order_id)
            payment = Payment.objects.get(transaction_id=txnid)

            if (
                payment.order == order
                and payment.status == "PAYMENT_SUCCESS"
                and order.is_verified
                and not order.is_completed
            ):
                # messages.success(request, f"Order ID: {order.id}, User ID: {order.user.id}, Name: {order.user.name}, Order Amount: {order.total_amount}")
                # return redirect('dashboard')  # Redirect to admin dashboard after marking order as delivered
                order.is_completed = True
                order.save()
                status = "Order Delivered"
                response = HttpResponse(
                    f"Order ID: {order.id}, User ID: {order.user.id}, Name: {order.user.name}, Order Amount: {order.total_amount}, Order Status: {status}",
                )
                response.status_code = 200
                order_items = OrderItem.objects.filter(order=payment.order).all()
                prod_list = []
                for item in order_items:
                    prod_list.append(
                        {
                            "name": item.product.name,
                            "quantity": item.quantity,
                        }
                    )
                send_order_completion_email_async(
                    payment.transaction_id,
                    order.user.name,
                    order.updated_amount,
                    prod_list,
                    order.user.email,
                )
                return response

            response = HttpResponse("QR code already used or order not verified")
            response.status_code = 400
            return response

        except Order.DoesNotExist:
            response = HttpResponse("Order not found")
            response.status_code = 400
            return response
        except Payment.DoesNotExist:
            response = HttpResponse("Payment not found")
            response.status_code = 400
            return response
        except ValueError:
            response = HttpResponse("Invalid QR code")
            response.status_code = 400
            return response
    # return render(request, 'dashboard/scan_qr.html')


@staff_member_required
def successful_order_csv(request, id):
    if request.method == "GET":
        raise Http404

    items = OrderItem.objects.filter(product__pk=id, order__is_verified=True)
    if not items:
        raise Http404("OrderItem not found.")

    first_row = ["Name", "Email Id", "Phone Number", "Position", "Quantity"]
    rows = [first_row]

    for item in items:
        user = item.order.user
        row = [user.name, user.email, user.phone_no, user.position, item.quantity]

        if item.product.is_size_required:
            first_row.append("Size")
            row.append(item.size)
        if item.product.is_name_required:
            first_row.append("Printing Name")
            row.append(item.printing_name)
        if item.product.is_image_required:
            first_row.append("Image URL")
            row.append(item.image_url)

        rows.append(row)

    pseudo_buffers = Echo()
    writer = csv.writer(pseudo_buffers)
    return StreamingHttpResponse(
        (writer.writerow(row) for row in rows),
        content_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{item.product.name}_{item.product.pk}_successful_orders.csv"'
        },
    )
