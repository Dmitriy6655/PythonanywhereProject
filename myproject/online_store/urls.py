from django.urls import path
from online_store import views
from .views import all_clients, orders_by_client, order_full, upload_images, upload_images1

# edit_good,

app_name = 'online_store'

urlpatterns = [
    path('', all_clients, name="all_clients"),
    path('main/', views.main, name='main'),
    path('clients/', views.get_clients, name='clients'),
    path('goods/', views.get_goods, name='goods'),
    path('orders/', views.get_orders, name='orders'),
    path('client_orders/<int:client_id>', views.get_orders_by_client_id, name='client_orders'),
    path('delete_client/<int:client_id>', views.delete_client, name='delete_client'),
    path('delete_goods/<int:goods_id>', views.delete_goods, name='delete_goods'),
    path('delete_order/<int:order_id>', views.delete_order, name='delete_order'),
    path('edit_order_goods_id/<int:order_id>/<int:goods_id>', views.edit_order_goods_id, name='edit_order_goods_id'),
    path('client_goods/', views.client_goods, name='client_goods'),
    path("edit/", views.get_edit_good, name="get_edit_good"),
    path("order/<int:order_pk>", order_full, name="order_full"),

]
