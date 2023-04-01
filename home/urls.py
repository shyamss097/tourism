
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('packages/', views.packages_list, name='packages_list'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/signup/', views.user_signup, name='user_signup'),
    path('manager/signup/', views.manager_signup, name='manager_signup'),
    path('user/login/', views.user_login, name='user_login'),
    path('manager/login/', views.manager_login, name='manager_login'),
    #path('logout/', views.logout_view, name='logout'),
]
