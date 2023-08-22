from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, LoginForm
from .models import Transaction
from django.contrib.auth.decorators import login_required

@login_required
def list_transactions(request):
    search_query = request.GET.get('search', '')
    transactions = Transaction.objects.filter(user=request.user, type__icontains=search_query)
    return render(request, 'transaction_list.html', {'transactions': transactions})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)  # Hash the password
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to the login page
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
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

def logout_view(request):
    logout(request)
    return redirect('login')