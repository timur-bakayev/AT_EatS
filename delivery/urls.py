from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create_establishment/', views.create_establishment, name='create_establishment'),
    path('detail/<int:pk>/', views.detail_establishment, name='detail_establishment'),
    path('create_food/', views.create_food, name='create_food'),
    path('detail_food/<int:pk>', views.detail_food, name='detail_food'),
    path('cart/', views.cart, name='cart'),
    path('customer_create/', views.customer_create, name='customer_create'),
    path('delete_cart_item/<int:pk>', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart_item/<int:pk>', views.edit_cart_item, name='edit_cart_item'),
    path('cart/create_order', views.create_order, name='create_order'),
    path('establishment_orders/', views.establishment_orders, name='establishment_orders'),
    path('edit_food/<int:pk>', views.edit_food, name='edit_food'),
    path('delete_food/<int:pk>', views.delete_food, name='delete_food'),
    path('is_success/<int:pk>', views.is_success, name='is_success'),

]
