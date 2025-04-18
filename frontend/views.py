from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from backend.models import Loan, Fine, Reservation, Book
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