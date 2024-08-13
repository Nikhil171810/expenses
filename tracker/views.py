from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Transaction
from .forms import TransactionForm, ReportForm
from django.db.models import Sum, Avg
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Avg, F

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# Registration view
def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(Q(email=email) | Q(username=username))

        if user_obj.exists():
            messages.error(request, 'Error: Username or Email already exists')
            return redirect('registration')
        
        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email    
        )
        user_obj.set_password(password)
        user_obj.save()
        # user_obj = authenticate(username=username, password=password)
        
        # messages.success(request, 'Success: Account created')
        # return redirect('login_page')
        return login_page(request)

    return render(request, 'registration.html')

# Login view
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        
        if not user_obj.exists():
            messages.error(request, 'Error: Username does not exist')
            return redirect('login')

        refresh = RefreshToken.for_user(user_obj.first())
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        print(access_token)

        # return JsonResponse({
        #     'access_token': access_token,
        #     'refresh_token': refresh_token
        # }, status=200)

        user_obj = authenticate(username=username, password=password)

        if not user_obj:
            messages.error(request, 'Error: Invalid credentials')
            return redirect('login')
        
        login(request, user_obj)
        return redirect('home')

    return render(request, 'login.html')

# Logout view
def logout_page(request):
    logout(request)
    messages.success(request, 'Success: Logged out successfully')
    return redirect('login_page')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def view_expense(request):
    transactions = Transaction.objects.filter(created_by=request.user)
    return render(request, 'view_expense.html', {'transactions': transactions})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.created_by = request.user
            transaction.save()
            return redirect('view_expense')
    else:
        form = TransactionForm()
    return render(request, 'add_expense.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('view_expense'))
    else:
        form = TransactionForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def edit_expense(request, id):
    transaction = Transaction.objects.get(id=id, created_by=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully')
            return redirect('view_expense')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_expense.html', {'form': form, 'transaction': transaction})

@login_required
def delete_expense(request, id):
    queryset = Transaction.objects.get(id=id)
    queryset.delete()
    return redirect('view_expense')


@login_required
def generate_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            user_expenses = Transaction.objects.filter(date__range=[start_date, end_date], created_by=request.user)
            cat_expenses = user_expenses.values('category').annotate(total_amount=Sum('amount'))
            


            # Calculate overall total and average amounts
            overall_totals = cat_expenses.aggregate(overall_total=Sum('amount'), overall_avg=Avg('amount'))
            overall_total_amount = overall_totals['overall_total'] or 0.0
            overall_average_amount = overall_totals['overall_avg'] or 0.0

            return render(request, 'report.html', {
                'user_expenses':user_expenses,
                'total_amount': "{:.2f}".format(overall_total_amount),
                'average_amount': "{:.2f}".format(overall_average_amount),
                'cat_expenses':cat_expenses,
                'start_date': start_date,
                'end_date': end_date
            })
    else:
        form = ReportForm()
    
    return render(request, 'generate_report.html', {'form': form})

def generate_pdf(request):
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expense_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica", 16)
    p.drawString(100, 750, "Expense Report")


    expenses = Transaction.objects.filter(created_by=request.user)
    y = 700
    for expense in expenses:
        p.setFont("Helvetica", 12)
        p.drawString(100, y, f"{expense.date} - {expense.description}: {expense.amount}")
        y -= 20

    p.showPage()
    p.save()
    return response
