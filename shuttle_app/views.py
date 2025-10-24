# shuttle_app/views.py
from .models import AuthLog, Booking

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
from django.contrib.auth.decorators import user_passes_test
import json

from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from django.shortcuts import render, get_object_or_404




# ---------------------------
# Main Pages
# ---------------------------
def home(request):
    return render(request, 'index.html')

def booking(request):
    username = request.user.username if request.user.is_authenticated else ""
    return render(request, 'booking.html', {'username': username})

def operator(request):
    return render(request, 'operator.html')

def track2(request):
    return render(request, 'track2.html')

def about(request):
    return render(request, 'about.html')

# ---------------------------
# User Dashboard (optional)
# ---------------------------
def auth_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    logs = []
    return render(request, 'dashboard.html', {'logs': logs})

# ---------------------------
# AJAX Login
# ---------------------------
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "message": "Invalid credentials"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})

# ---------------------------
# AJAX Signup
# ---------------------------
@csrf_exempt
def signup_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")
            if User.objects.filter(username=username).exists():
                return JsonResponse({"success": False, "message": "Username already taken"})
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})

# ---------------------------
# Logout
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

# ===================================================
#                  ADMIN SECTION
# ===================================================

# ---------------------------
# Admin Login Page
# ---------------------------
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials or not authorized")
            return redirect('admin_login')

    return render(request, 'admin/admin_login.html')

# ---------------------------
# Admin Signup Page
# ---------------------------
def admin_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Admin username already exists")
            return redirect('admin_signup')

        user = User.objects.create_user(username=username, password=password, is_staff=True)
        user.save()
        messages.success(request, "Admin created successfully! Please log in.")
        return redirect('admin_login')

    return render(request, 'admin/admin_signup.html')

# ---------------------------
# Admin Dashboard (with logs)
# ---------------------------

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    from .models import Booking

    # --- Core Stats ---
    total_users = User.objects.count()
    total_bookings = Booking.objects.count()
    total_seats = Booking.objects.aggregate(total=Sum('seats'))['total'] or 0

    # Mock fare rate per seat (you can replace this later)
    fare_per_seat = 50
    total_revenue = total_seats * fare_per_seat

    # --- Top 3 Zones ---
    zone_stats = (
        Booking.objects.values('zone')
        .annotate(count=Count('id'))
        .order_by('-count')[:3]
    )

    # --- Top 3 Routes ---
    route_stats = (
        Booking.objects.values('pickup_location', 'drop_location')
        .annotate(count=Count('id'))
        .order_by('-count')[:3]
    )

    # --- Last 7 Days Trend ---
    today = timezone.now().date()
    trend_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        count = Booking.objects.filter(created_at__date=day).count()
        trend_data.append({'date': day.strftime('%b %d'), 'count': count})

    # --- Latest Logs ---
    logs = AuthLog.objects.order_by('-timestamp')[:10]

    context = {
        'total_users': total_users,
        'total_bookings': total_bookings,
        'total_seats': total_seats,
        'total_revenue': total_revenue,
        'zone_stats': zone_stats,
        'route_stats': route_stats,
        'trend_data': trend_data,
        'logs': logs,
    }

    return render(request, 'admin/admin_dashboard.html', context)


# ---------------------------
# Admin Logs Page (optional)
# ---------------------------
# @user_passes_test(lambda u: u.is_staff)
# def admin_logs(request):
#     logs = AuthLog.objects.order_by('-timestamp')[:100]  # Latest 100 logs
#     return render(request, 'admin/admin_logs.html', {'logs': logs})

@user_passes_test(lambda u: u.is_staff)
def admin_logs(request):
    event_filter = request.GET.get('event', '')
    if event_filter:
        logs = AuthLog.objects.filter(event=event_filter).order_by('-timestamp')[:100]
    else:
        logs = AuthLog.objects.all().order_by('-timestamp')[:100]
    return render(request, 'admin/admin_logs.html', {'logs': logs})



                                                        # booking backend


# ---------------------------
# Admin Booking Management
# ---------------------------

# shuttle_app/views.py


from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Sum
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from .models import Booking

@user_passes_test(lambda u: u.is_staff)
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')

    # --- Filters ---
    zone_filter = request.GET.get('zone', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    if zone_filter:
        bookings = bookings.filter(zone=zone_filter)
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if date_filter:
        now = timezone.now()
        if date_filter == 'today':
            bookings = bookings.filter(created_at__date=now.date())
        elif date_filter == 'week':
            bookings = bookings.filter(created_at__gte=now - timedelta(days=7))
        elif date_filter == 'month':
            bookings = bookings.filter(created_at__gte=now - timedelta(days=30))

    # --- Analytics ---
    total_bookings = bookings.count()
    approved_count = bookings.filter(status='Approved').count()
    pending_count = bookings.filter(status='Pending').count()
    cancelled_count = bookings.filter(status='Canceled').count()
    total_seats = bookings.aggregate(total_seats=Sum('seats'))['total_seats'] or 0

    # --- Charts ---
    zone_counts = bookings.values('zone').annotate(count=Count('id'))
    zone_chart = {z['zone']: z['count'] for z in zone_counts}

    payment_counts = bookings.values('payment_method').annotate(count=Count('id'))
    payment_chart = {p['payment_method']: p['count'] for p in payment_counts}

    # --- Recent Bookings ---
    recent_bookings = bookings[:10]

    # --- Distinct Zones ---
    zones = Booking.objects.values_list('zone', flat=True).distinct()

    context = {
        'bookings': bookings,
        'zones': zones,
        'zone_filter': zone_filter,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'total_bookings': total_bookings,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'total_seats': total_seats,
        'zone_chart_labels': list(zone_chart.keys()),
        'zone_chart_values': list(zone_chart.values()),
        'payment_chart_labels': list(payment_chart.keys()),
        'payment_chart_values': list(payment_chart.values()),
        'recent_bookings': recent_bookings,
    }

    return render(request, 'admin/admin_bookings.html', context)







# ---------------------------
# Booking Status Update (Approve / Cancel)
# ---------------------------

@user_passes_test(lambda u: u.is_staff)
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Approved'
    booking.save()
    return redirect('admin_bookings')


@user_passes_test(lambda u: u.is_staff)
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Canceled'
    booking.save()
    return redirect('admin_bookings')



@csrf_exempt
@user_passes_test(lambda u: u.is_staff)
def update_booking_status(request, booking_id):
    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            status = data.get("status")
            booking = get_object_or_404(Booking, id=booking_id)
            booking.status = status
            booking.save()

            # Updated counts, charts & recent bookings
            bookings = Booking.objects.all()
            counts = {
                "approved": bookings.filter(status="Approved").count(),
                "pending": bookings.filter(status="Pending").count(),
                "canceled": bookings.filter(status="Canceled").count(),
                "total": bookings.count(),
                "total_seats": bookings.aggregate(total_seats=Sum('seats'))['total_seats'] or 0
            }

            zone_counts = bookings.values('zone').annotate(count=Count('id'))
            zone_chart = {"labels":[z['zone'] for z in zone_counts], "values":[z['count'] for z in zone_counts]}

            payment_counts = bookings.values('payment_method').annotate(count=Count('id'))
            payment_chart = {"labels":[p['payment_method'] for p in payment_counts], "values":[p['count'] for p in payment_counts]}

            recent_bookings = list(bookings.order_by('-created_at')[:10].values(
                'id', 'passenger_name', 'zone', 'pickup_location', 'drop_location', 
                'seats', 'payment_method', 'status', 'created_at'
            ))
            for b in recent_bookings:
                b['created_at'] = b['created_at'].strftime("%b %d, %Y %H:%M")

            return JsonResponse({"success": True, "counts": counts, "zone_chart": zone_chart, "payment_chart": payment_chart, "recent_bookings": recent_bookings})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})



@csrf_exempt
def create_booking(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"success": False, "message": "Login required"})
        try:
            data = json.loads(request.body)
            booking = Booking.objects.create(
                passenger=request.user,
                passenger_name=data.get('passenger_name', request.user.username),
                zone=data.get('zone'),
                pickup_location=data.get('pickup_location'),
                drop_location=data.get('drop_location'),
                seats=data.get('seats', 1),
                payment_method=data.get('payment_method', 'UPI'),
                status='Confirmed'
            )
            return JsonResponse({"success": True, "booking_id": booking.id})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
    return JsonResponse({"success": False, "message": "Invalid request"})


@csrf_exempt
# shuttle_app/views.py

# ---------------------------
# Admin Booking Management
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')

    # Filters
    zone_filter = request.GET.get('zone', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    if zone_filter:
        bookings = bookings.filter(zone=zone_filter)
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if date_filter:
        now = timezone.now()
        if date_filter == 'today':
            bookings = bookings.filter(created_at__date=now.date())
        elif date_filter == 'week':
            bookings = bookings.filter(created_at__gte=now - timedelta(days=7))
        elif date_filter == 'month':
            bookings = bookings.filter(created_at__gte=now - timedelta(days=30))

    # Analytics
    total_bookings = bookings.count()
    approved_count = bookings.filter(status='Approved').count()
    pending_count = bookings.filter(status='Pending').count()
    cancelled_count = bookings.filter(status='Canceled').count()
    total_seats = bookings.aggregate(total_seats=Sum('seats'))['total_seats'] or 0

    # Charts
    zone_counts = bookings.values('zone').annotate(count=Count('id'))
    zone_chart = {z['zone']: z['count'] for z in zone_counts}

    payment_counts = bookings.values('payment_method').annotate(count=Count('id'))
    payment_chart = {p['payment_method']: p['count'] for p in payment_counts}

    # Recent bookings
    recent_bookings = bookings[:10]

    # Zones for filter dropdown
    zones = Booking.objects.values_list('zone', flat=True).distinct()

    context = {
        'zones': zones,
        'zone_filter': zone_filter,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'total_bookings': total_bookings,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'cancelled_count': cancelled_count,
        'total_seats': total_seats,
        'zone_chart_labels': list(zone_chart.keys()),
        'zone_chart_values': list(zone_chart.values()),
        'payment_chart_labels': list(payment_chart.keys()),
        'payment_chart_values': list(payment_chart.values()),
        'recent_bookings': recent_bookings,
    }
    return render(request, 'admin/admin_bookings.html', context)

# ---------------------------
# Fetch Latest Bookings (AJAX)
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def fetch_latest_bookings(request):
    bookings = Booking.objects.order_by('-created_at')[:10]
    data = []
    for b in bookings:
        data.append({
            "id": b.id,
            "passenger_name": b.passenger_name,
            "zone": b.zone,
            "pickup": b.pickup_location,
            "drop": b.drop_location,
            "seats": b.seats,
            "payment": b.payment_method,
            "status": b.status,
            "created": b.created_at.strftime("%b %d, %Y %H:%M")
        })

    # Also return counts and chart data
    all_bookings = Booking.objects.all()
    counts = {
        "total": all_bookings.count(),
        "approved": all_bookings.filter(status="Confirmed").count(),
        "pending": all_bookings.filter(status="Pending").count(),
        "canceled": all_bookings.filter(status="Canceled").count(),
    }

    zone_counts = all_bookings.values('zone').annotate(count=Count('id'))
    zone_chart = {
        "labels": [z['zone'] for z in zone_counts],
        "values": [z['count'] for z in zone_counts]
    }

    payment_counts = all_bookings.values('payment_method').annotate(count=Count('id'))
    payment_chart = {
        "labels": [p['payment_method'] for p in payment_counts],
        "values": [p['count'] for p in payment_counts]
    }

    return JsonResponse({
        "bookings": data,
        "counts": counts,
        "zone_chart": zone_chart,
        "payment_chart": payment_chart
    })


# ---------------------------
# Cancel Booking (AJAX)
# ---------------------------
@user_passes_test(lambda u: u.is_staff)
def cancel_booking(request, booking_id):
    if request.method == "POST":
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = "Canceled"
        booking.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request"})
