from django.db import IntegrityError
from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category,Product,Customer,Order,OrderItem
from django.shortcuts import get_object_or_404
from django.urls  import reverse
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request,'base/home.html')

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
    return render(request, "registration/login_page.html", {"form": form})

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return redirect('home')  
            
    return render(request, 'login.html')
def logout(request):
    auth_logout(request)  # Logs the user out
    messages.success(request, "You have been logged out successfully.")  # Add success message
    return redirect("login") 

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.save()
            login(request,user)
            return redirect('home')
            messages.success(request,"Account Created successful")
            # Optionally, you can add any additional actions after saving the user here
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def categories(request):
    return render(request,'base/categories.html')

def category(request,name):
    category=get_object_or_404(Category,name=name)
    if category.name=='Dining':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    
    elif category.name=='Living':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    elif category.name=='Bedroom':
        product=Product.objects.filter(category=category)
        product_name=category.name
        return render(request,'base/bedroom.html',
                  {
                      'product':product,
                      "product_name":product_name,
                  })
    
    else:
        return HttpResponse("Error")
    
#product description
def description(request,name):
    description=Product.objects.filter(name=name)
    return render(request,"base/product-description.html",
                  {
                      "description":description,
                      
                  })
#listing all the product in products page

def product_list(request):
    
    if request.user:
        product=Product.objects.all()
        return render(request,"base/product_list.html",{
            "product":product
        })
    else:
        return redirect("login")

@login_required
def add_to_cart(request, product_id):
    customer, created = Customer.objects.get_or_create(user=request.user)
    if customer is None:
        messages.info(request,"Item added to cart")
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, user=request.user)
    order_item.quantity += 1
    messages.info(request,f"{product.name} added to cart")
    order_item.save()
    return redirect('product_list')
    

def view_cart(request):
    customer = get_object_or_404(Customer, user=request.user)
    items=OrderItem.objects.filter(user=request.user)
    order = get_object_or_404(Order, customer=customer, complete=False)
    total_amount =order.get_cart_total
    return render(request, 'base/cart.html', {"items": items,"total_amount":total_amount})


def remove_item(request,product_id):
    items=OrderItem.objects.get(id=product_id)
    messages.warning(request,f"{items.product.name} got removed.")
    items.delete()
    return redirect('cart')

#incrementing and Decrementing 
def cart_quantity(request,product_id):
    items=OrderItem.objects.get(id=product_id)
    if 'increment' in request.GET:
        items.quantity+=1
        items.save()
        print(items.quantity)
    elif 'decrement' in request.GET:
        if items.quantity==1:
            remove_item(request,product_id)
        else:
            items.quantity-=1
            items.save()
    else:
        messages.error("Error")
    return redirect('cart')


#after clicking direct BUY NOW 
@login_required
def buy_now(request,product_id):
    customer, created = Customer.objects.get_or_create(user=request.user)
    if customer is None:
        messages.info(request,"Item added to cart")
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, user=request.user)
    order_item.quantity += 1
    messages.info(request,f"{product.name} added to cart")
    order_item.save()
    return redirect('cart')


import hmac
import hashlib
import base64

def signature(secret, message):
    secret_bytes = bytes(secret, 'utf-8')
    message_bytes = bytes(message, 'utf-8')
    
    hmac_obj = hmac.new(secret_bytes, message_bytes, hashlib.sha256)
    hmac_digest = hmac_obj.digest()
    
    hash = base64.b64encode(hmac_digest).decode()
    return hash

# Example usage
secret = "your_secret_key"
message = "your_message"
print(signature(secret, message))


@login_required
def checkout(request):
    customer = get_object_or_404(Customer, user=request.user)
    items = OrderItem.objects.filter(user=request.user)
    order = get_object_or_404(Order, customer=customer, complete=False)
    total_amount = order.get_cart_total
    messages = f"{total_amount},{order.transaction_id},{{order.id}}"
    print(order.id)
    
    print("Data used for signature:", messages)  # Debugging log
    hash = signature("8gBm/:&EnhH.1/q", messages)
    
    print("Generated signature:", hash)  # Debugging log
    print(total_amount)
    print(f"Transaction:{order.transaction_id}")
    
    return render(request, 'base/checkout.html', {
        'items': items,
        'total_amount': total_amount,
        'transaction_id':order.transaction_id,
        'signature': hash,
        'order':order
    })