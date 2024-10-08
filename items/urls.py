from django.contrib import admin
from django.urls import path
from items import views

urlpatterns = [
    path("admin", admin.site.urls),
    path("add_to_cart", views.add_to_cart, name='add_to_cart'),
    path("cart", views.cart, name='cart'),
    path('<int:pk>/delete_from_cart', views.delete_from_cart, name='delete_from_cart'),
    path('<int:pk>/update_quantity', views.update_quantity, name='update_quantity'),
    path('order', views.order, name='order'),
    path('orders', views.orders, name='orders'),
]