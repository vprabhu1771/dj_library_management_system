from datetime import date

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from backend.models import Loan, Fine, Reservation, Book, FinePayment
from frontend.forms import RegisterForm, LoginForm


from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

import razorpay

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Create your views here.
def home(request):
    return render(request, "frontend/home.html")

def books_list(request):
    context = {
        'books': Book.objects.all()
    }
    return render(request, "frontend/books.html", context)

# Member Registration
def member_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('member_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'frontend/register.html', {'form': form})

# Member Login
def member_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('member_dashboard')
    else:
        form = LoginForm()
    return render(request, 'frontend/login.html', {'form': form})


# Logout
def member_logout(request):
    logout(request)
    return redirect('login')


# Dashboard (Optional)
@login_required
def member_dashboard(request):
    user = request.user

    total_book_loans = Loan.objects.filter(member_id=user).count()
    total_fine = Fine.objects.filter(member=user).aggregate(total=Sum('fine_amount'))['total'] or 0
    books_reserved = Reservation.objects.filter(member=user).count()

    context = {
        'total_book_loans': total_book_loans,
        'total_fine': total_fine,
        'books_reserved': books_reserved,
    }

    return render(request, 'frontend/dashboard.html', context)

# List of Loaned Books
@login_required
def loaned_books(request):
    loans = Loan.objects.filter(member=request.user)
    return render(request, 'frontend/loaned_books.html', {'loans': loans})

# List of Fines
@login_required
def fines_view(request):
    fines = Fine.objects.filter(member=request.user)
    return render(request, 'frontend/fines.html', {'fines': fines})

# Razorpay Payment View
@login_required
def pay_fine(request, fine_id):
    fine = Fine.objects.get(id=fine_id)

    if request.method == "POST":
        # Create an order in Razorpay

        # Razorpay works with paise, so multiply by 100
        amount_in_paise = int(fine.fine_amount * 100)   # Convert Decimal to int (paise)
        order = razorpay_client.order.create(dict(
            amount=amount_in_paise,  # Amount in paise
            currency='INR',
            # payment_capture='1'  # 1 means automatic capture
        ))

        context = {
            'order_id': order['id'],
            'amount': fine.fine_amount,
            'amount_in_paise': amount_in_paise,
            'fine_id': fine.id,
            'razorpay_key': RAZORPAY_KEY_ID,
        }

        return render(request, 'frontend/payment_page.html', context)

    return redirect('fines')

# Razorpay Payment Success Callback
@csrf_exempt  # Razorpay posts from external domain
def payment_success(request):
    if request.method == 'POST':
        try:
            # Razorpay sends these in POST
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            fine_id = request.POST.get('fine_id')

            # Signature verification
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            razorpay_client.utility.verify_payment_signature(params_dict)

            # If no exception, proceed
            fine = Fine.objects.get(id=fine_id, member=request.user)

            FinePayment.objects.create(
                member=request.user,
                payment_date=date.today(),
                payment_amount=fine.fine_amount
            )

            # ✅ Mark the fine as paid instead of deleting it
            fine.status = 'Paid'
            fine.save()

            return render(request, 'frontend/payment_success.html', {
                'amount': fine.fine_amount
            })

        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed.")

    return redirect('fines')

# View Reservations
@login_required
def reservations_view(request):
    reservations = Reservation.objects.filter(member=request.user)
    return render(request, 'frontend/reservations.html', {'reservations': reservations})

# Book Reservation
@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    Reservation.objects.create(
        book=book,
        member=request.user,
        reservation_date=date.today(),
    )
    return redirect('reservations')