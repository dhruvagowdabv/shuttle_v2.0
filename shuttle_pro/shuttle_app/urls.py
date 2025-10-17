from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('operator/', views.operator, name='operator'),
    path('track2/', views.track2, name='track2'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin, name='admin'),

    # Auth endpoints for AJAX
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.auth_dashboard, name='dashboard'),
]
