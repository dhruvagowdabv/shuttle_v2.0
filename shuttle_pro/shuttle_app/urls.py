from django.urls import path
from . import views


urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('operator/', views.operator, name='operator'),
    path('track2/', views.track2, name='track2'),
    path('about/', views.about, name='about'),

    # User auth AJAX
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Admin pages
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/signup/', views.admin_signup, name='admin_signup'),
    path('admin-panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/logs/', views.admin_logs, name='admin_logs'),

    # Optional user dashboard
    path('dashboard/', views.auth_dashboard, name='dashboard'),


    # booking backend
    path('api/create-booking/', views.create_booking, name='create_booking'),

    # Admin Booking Page
    path('admin-panel/bookings/', views.admin_bookings, name='admin_bookings'),




    # path('admin-panel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-panel/bookings/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('admin-panel/bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),

    path('admin-panel/bookings/update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),

    path('fetch-latest-bookings/', views.fetch_latest_bookings, name='fetch_latest_bookings'),

    # path('admin-panel/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin-panel/bookings/fetch_latest/', views.fetch_latest_bookings, name='fetch_latest_bookings'),
    path('admin-panel/bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),


]
