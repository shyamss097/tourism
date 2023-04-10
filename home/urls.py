
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('search/', views.search_destination, name='search_destination'),
    path('about/', views.aboutpage, name='about'),
    path('contact/', views.contactpage, name='contact'),
    #path('packages/', views.packages_list, name='packages_list'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    # path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    
    #path('add-to-cart/<int:package_id>/', views.add_to_cart, name='add_to_cart'),
    # path('checkout/<int:package_id>/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    # path('order/<int:pk>', views.order, name='order'),
    path('ticket/<int:cart_id>/<int:package_id>/', views.ticket1, name='ticket'),
    # path('billing/', views.billing, name='billing'),
    # path('remove-from-cart/<int:package_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('orders', views.orders, name='orders'),
    path('cancel_order/<str:order_id>', views.cancel_order, name='cancel_order'),
    path('user/signup/', views.register, name='user_signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
