from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import Transaction
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def list_transactions(request):
    try:
        search_query = request.GET.get('search', '')
        transactions_list = Transaction.objects.filter(user=request.user, type__icontains=search_query)

        # Pagination
        paginator = Paginator(transactions_list, 5)  # Show 25 transactions per page
        page = request.GET.get('page')
        try:
            transactions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            transactions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            transactions = paginator.page(paginator.num_pages)

        return render(request, 'transaction_list.html', {'transactions': transactions})

    except DatabaseError:
        messages.error(request, "An error occurred while fetching transactions.")
        return redirect('transactions')

def signup_view(request):
    try:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)  # Hash the password
                user.save()
                login(request, user)
                return redirect('login')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    except DatabaseError:
        messages.error(request, "An error occurred during signup. Please try again.")
        return redirect('signup')

def login_view(request):
    try:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                if user:
                    login(request, user)
                    return redirect('transactions')  
                else:
                    messages.error(request, "Incorrect username or password.")
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')

def logout_view(request):
    try:
        logout(request)
    except Exception as e:
        messages.error(request, str(e))
    return redirect('login')