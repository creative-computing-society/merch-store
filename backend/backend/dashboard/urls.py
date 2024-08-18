from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="admin_dashboard"),
    path("stop-orders/", views.stopOrders, name="stop_orders"),
    path("start-orders/", views.startOrders, name="start_orders"),
    path("discount-codes/", views.discount_codes, name="discount_codes"),
    path(
        "discount-codes/create/",
        views.create_discount_code,
        name="create_discount_code",
    ),
    path(
        "discount-codes/edit/<int:code_id>/",
        views.edit_discount_code,
        name="edit_discount_code",
    ),
    path(
        "discount-codes/delete/<int:code_id>/",
        views.delete_discount_code,
        name="delete_discount_code",
    ),
    path("products/", views.products, name="products"),
    path("products/create/", views.create_product, name="create_product"),
    path("products/edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path(
        "products/delete/<int:product_id>/", views.delete_product, name="delete_product"
    ),
    path("scan_qr/", views.render_qr_page, name="scan_qr_page"),
    path("scan_qr/scan/", views.scan_qr, name="scan_qr"),
    path("export_csv/<int:id>/", views.successful_order_csv, name="export_csv"),
]
