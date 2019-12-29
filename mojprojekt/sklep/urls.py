from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('products/', views.product_list),
    path('products/<int:product_id>',views.detail),
    path("order/<int:order_id>",views.order_details),
    path("order/", views.order),
    path("complaint/",views.complaint),
    path("complaint/<int:complaint_id>",views.complaint_details),
    path("cart/", views.cart),
    path("cart/add/", views.add_to_cart),
    path("cart/remove/",views.remove_from_cart),
    path("cart/modify/", views.modify_cart),
    path("products/<int:product_id>/comment", views.comment),
    path("products/<int:product_id>/comments", views.comments_detail)
]