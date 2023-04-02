
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    #path('packages/', views.packages_list, name='packages_list'),
    # path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    # path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/signup/', views.register, name='user_signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
