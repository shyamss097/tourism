from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def homepage(request):
    packages = Package.objects.all()

    return render(request, 'base.html', {'packages': packages})

def aboutpage(request):
    return render(request, 'about.html')
def contactpage(request):
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_manager = form.cleaned_data['is_manager']
            user.save()
            # authenticate and log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # redirect to appropriate dashboard
            if user.is_manager:
                return redirect('home')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') # Replace 'home' with your desired redirect URL
        else:
            # Show an error message if authentication fails
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


def package_list(request):
    packages = Package.objects.all()
    return render(request, 'package_list.html', {'packages': packages})



@login_required
def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)

    if request.method == 'POST':
        # get selected accommodation and its price
        accommodation_id = request.POST.get('accommodation')
        if accommodation_id:
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            request.session['selected_accommodation'] = {
                'id': accommodation.id,
                'name': accommodation.name,
                'price': accommodation.price
            }
        else:
            request.session.pop('selected_accommodation', None)

        # get selected food and its price
        food_id = request.POST.get('food')
        if food_id:
            food = get_object_or_404(Food, pk=food_id)
            request.session['selected_food'] = {
                'id': food.id,
                'name': food.name,
                'price': food.price
            }
        else:
            request.session.pop('selected_food', None)

        return redirect('cart')

    # render template with package details and form to select food and accommodation
    accommodations = Accommodation.objects.all()
    foods = Food.objects.all()
    return render(request, 'package_detail.html', {
        'package': package,
        'accommodations': accommodations,
        'foods': foods,
    })


def cart(request):
    package = get_object_or_404(Package, pk=request.session['selected_package']['id'])

    selected_accommodation = request.session.get('selected_accommodation')
    selected_food = request.session.get('selected_food')

    total_duration = package.duration
    total_accommodation_cost = selected_accommodation['price'] * total_duration if selected_accommodation else 0
    total_food_cost = selected_food['price'] * total_duration * 3 if selected_food else 0
    total_cost = package.price + total_accommodation_cost + total_food_cost

    return render(request, 'cart.html', {
        'package': package,
        'selected_accommodation': selected_accommodation,
        'selected_food': selected_food,
        'total_duration': total_duration,
        'total_accommodation_cost': total_accommodation_cost,
        'total_food_cost': total_food_cost,
        'total_cost': total_cost,
    })

def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    
   
    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)

def get_cart_total_price(cart):
    total_price = 0
    for item in cart.cartitem_set.all():
        total_price += item.total_price
    return total_price

# @login_required
# def checkout(request, pk):
#     package = get_object_or_404(Package, pk=pk)
#     cart = request.user.cart
#     duration = package.duration
#     selected_foods = cart.food.all()
#     selected_accommodation = cart.accommodation
#     food_cost = sum([food.price for food in selected_foods]) * duration * 3  # 3 meals per day
#     accommodation_cost = selected_accommodation.price * duration
#     total_price = package.price + food_cost + accommodation_cost
#     order = Order.objects.create(user=request.user, package=package, total_price=total_price)
#     cart.delete()
#     return render(request, 'checkout.html', {'order': order})

@login_required
def checkout(request, package_id):
    user = request.user
    cart = user.cart

    if not cart.items.exists():
        return redirect('view-cart')

    package = get_object_or_404(Package, id=package_id)

    food_cost = sum([item.food.price for item in cart.items.all()]) * package.duration * 3
    accommodation_cost = sum([item.accommodation.price for item in cart.items.all()]) * package.duration

    total_price = food_cost + accommodation_cost + package.price

    # create the order
    order = user.orders.create(package=package, total_price=total_price)

    # save the cart items to the order
    for item in cart.items.all():
        order.items.create(package=item.package, duration=item.duration, food=item.food, accommodation=item.accommodation, total_price=item.total_price)

    # clear the cart
    cart.items.all().delete()

    # render the ticket template
    return render(request, 'ticket.html', {'order': order})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('view-cart')
    context = {
        'cart_item': cart_item
    }
    return render(request, 'remove_from_cart.html', context)
