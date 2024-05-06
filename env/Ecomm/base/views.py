from django.shortcuts import render,redirect,HttpResponse
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'base/home.html')

def store(request):
    context={}
    return render(request,'base/store.html',context)

def cart(request):
    context={}
    return render(request,'base/cart.html',context)


def login_view(request):
# Redirect logged-in users
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user with form data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)  # Only call login if user is valid
                return redirect("home")
            elif user is not None and not user.is_active:
                messages.error(request, "Account is inactive.")
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Form validation failed.")
    # If GET request or invalid POST, render the login page with form
    form = LoginForm()  # Create an empty form
    return render(request, "registration\login_page.html", {"form": form})

def logout(request):
    auth_logout(request)  # Logs the user out
    messages.success(request, "You have been logged out successfully.")  # Add success message
    return redirect("login") 

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the new user
            form.save()
            # Authenticate and log in the new user
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)  # Log the user in
                messages.success(request, "Registration successful!")  # Message indicating success
                return render(request,'base/home.html')  # Redirect to a desired page (e.g., home)

            messages.error(request, "Authentication failed. Please try again.")  # Message if authentication fails
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")  # Message if form is invalid

    # Render the registration form for GET requests or if the form is invalid
    form = RegisterForm()  # Create a new form instance
    return render(request, "registration/register.html", {"form": form})


def product(request):
    return render(request,'base/product.html')