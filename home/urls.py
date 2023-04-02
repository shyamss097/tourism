
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    #path('packages/', views.packages_list, name='packages_list'),
    # path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    # path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('add-to-cart/<int:package_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/<int:package_id>/', views.checkout, name='checkout'),
    path('cart/', views.view_cart, name='view-cart'),
    path('remove-from-cart/<int:package_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('user/signup/', views.register, name='user_signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
