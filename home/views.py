from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.utils.crypto import get_random_string
from reportlab.pdfgen import canvas
from io import BytesIO
from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def homepage(request):
    packages = Package.objects.all()
    if request.method == 'POST':
        search_flag = 1
        place = Places.objects.get(place = request.POST.get('destination'))
        search_packages = place.package
        print(search_packages)

        return render(request, 'home.html', {'search_flag': search_flag, 'search_packages': search_packages})


    return render(request, 'home.html', {'packages': packages})

def search_destination(request):
    search_flag = 1
    query = request.GET.get('location')
    places = Places.objects.filter(place__icontains=query)
    packages = []
    for place in places:
            for package in place.package.all():
                if package not in packages:
                    packages.append(package)
    print(places)
    search_packages = packages
    print(search_packages)
    return render(request, 'home.html', {'search_flag': search_flag, 'search_packages': search_packages, })

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


def package_detail(request, pk):
    package = Package.objects.get(pk=pk)
    # get all accommodations and their prices
    accommodations = Accommodation.objects.filter(package=pk).values('id', 'name', 'price')
    # get all foods and their prices
    foods = Food.objects.filter(package=pk).values('id', 'name', 'price')
    places = Places.objects.filter(package=package)
    

    if request.method == 'POST':
        print(request.POST)
        accommodation_id = request.POST.get('accommodation')
        if accommodation_id:
            accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
            accommodation_price = accommodation.price
        else:
            accommodation = None
            accommodation_price = 0

        food_id = request.POST.get('food')
        if food_id:
            food = get_object_or_404(Food, pk=food_id)
            food_price = food.price
        else:
            food = None
            food_price = 0
        
        
        total_price = package.price + accommodation_price * package.duration + food_price * 3 * package.duration
        if request.POST.get('action') == 'add_to_cart':
                # Add to cart and redirect to cart page
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart.package = package
            cart.food_id = food_id
            cart.accommodation_id = accommodation_id
            cart.total_price = total_price
            # cart = Cart.objects.create(
            #         user=request.user,
            #         package=package,
            #         food_id=food_id,
            #         accommodation_id=accommodation_id,
            #         total_price=total_price
            #     )
            cart.save()
            # cart.food.set(food)
            # cart.accommodation.set(accommodation)
            return render(request, 'cart.html', {'cart': cart, 'accommodations': accommodations, 'food': food, 'accommodation': accommodation, 'total_price': total_price, 'places': places})
        else:
            return render(request, 'package_detail.html', {'package': package, 'accommodations': accommodations, 'foods': foods, 'accommodation': accommodation, 'total_price': total_price, 'places': places})

    return render(request, 'package_detail.html', {'package': package, 'accommodations': accommodations, 'foods': foods, 'places': places})

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    food = None
    accommodation = None
    if cart.food_id:
        food = Food.objects.get(pk=cart.food_id)
    if cart.accommodation_id:
        accommodation = Accommodation.objects.get(pk=cart.accommodation_id)

    return render(request, 'cart.html', {'cart':cart, 'food': food, 'accommodation': accommodation})

def ticket(request, cart_id, package_id):
    if request.method == 'POST':

        cart = Cart.objects.get(id=cart_id)
        package = Package.objects.get(id=package_id)
        food = Food.objects.get(pk=cart.food_id)
        accommodation = Accommodation.objects.get(pk=cart.accommodation_id)    
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{request.user}.pdf"'

        # Get the template
        template = get_template('ticket.html')

        context = {'user': cart.user, 'package':package, 'food': food, 'accommodation': accommodation, 'duration': package.duration, 'total_price': cart.total_price, 'cart': cart}

        html = template.render(context)

        # Create the PDF document
        pisa_status = pisa.CreatePDF(html, dest=response)

        # If PDF creation failed, return an error message
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF ticket')

        cart.delete()
        return response
    
    
    cart = Cart.objects.get(pk=cart_id)
    package = Package.objects.get(pk=package_id)
    food = Food.objects.get(pk=cart.food_id)
    accommodation = Accommodation.objects.get(pk=cart.accommodation_id)
    print(accommodation.name)
    print(food.name)
     #total food price
    food_price = food.price * 3 * package.duration

    #total accommodation price
    accommodation_price = accommodation.price * package.duration

    #total price
    total_price = package.price + food_price + accommodation_price
        
    today = date.today()
    # Remove spaces and hyphens from package name
    package_name = package.name.replace(' ', '').replace('-', '')

        # Generate a random string to add at the end of the ID for uniqueness
    random_str = get_random_string(length=4)

    # Combine the first 4 characters of the package name and username and the random string
    order_id = f'{package_name[:3]}{request.user.username[:3]}{random_str}'

    order = Order.objects.create(order_id = order_id, user = request.user, package=package, food_price = food_price, accommodation_price = accommodation_price, total_price = total_price, created_at = today)
   
    context = {'user': cart.user, 'package':package, 'food': food, 'accommodation': accommodation, 'duration': package.duration, 'total_price': cart.total_price, 'order': order, 'cart': cart }
    cart.delete()
    
    return render(request, 'ticket.html', context)


def ticket1(request, cart_id, package_id):
    if request.method == 'POST':    
        cart = Cart.objects.get(id=cart_id)
        package = Package.objects.get(id=package_id)
        food = Food.objects.get(pk=cart.food_id)
        accommodation = Accommodation.objects.get(pk=cart.accommodation_id)   

         #total food price
        food_price = food.price * 3 * package.duration

        #total accommodation price
        accommodation_price = accommodation.price * package.duration

        #total price
        total_price = package.price + food_price + accommodation_price 

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="ticket_{request.user}.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        story = []

        # Create a style sheet for formatting text
        styles = getSampleStyleSheet()

        # Add a title with the package name
        title = Paragraph(f'<center><b>Ticket</b></center>', styles['Heading1'])
        
        story.append(title)
        story.append(Spacer(1, 10))
        pc = Paragraph(f'<b>{package.name} Package</b>', styles['Heading2'])
        
        story.append(pc)
        story.append(Spacer(1, 20))

       
        
        data = [
        ['User', request.user],
        ['Package', package.name],
        ['Package start date', package.start_date],
        ['Package start location', package.source],
        ['Food', food.name],
        ['Food(price per meal)', food.price],
        ['Accommodation', accommodation.name],
        ['Accommodation(price per day)', accommodation.price],
        ['Total Price', total_price],
    ]
        table = Table(data, colWidths=[doc.width/3]*2)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'whitesmoke'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))


        # Add a thank you message
        thank_you = Paragraph('Thank you for choosing our package! Enjoy your trip!', styles['BodyText'])
        story.append(thank_you)

        # Build the PDF document and return the response
        doc.build(story)
        cart.delete()
        return response


        
    
    
    cart = Cart.objects.get(pk=cart_id)
    package = Package.objects.get(pk=package_id)
    food = Food.objects.get(pk=cart.food_id)
    accommodation = Accommodation.objects.get(pk=cart.accommodation_id)
    print(accommodation.name)
    print(food.name)
     #total food price
    food_price = food.price * 3 * package.duration

    #total accommodation price
    accommodation_price = accommodation.price * package.duration

    #total price
    total_price = package.price + food_price + accommodation_price
        
    today = date.today()
    # Remove spaces and hyphens from package name
    package_name = package.name.replace(' ', '').replace('-', '')

        # Generate a random string to add at the end of the ID for uniqueness
    random_str = get_random_string(length=4)

    # Combine the first 4 characters of the package name and username and the random string
    order_id = f'{package_name[:3]}{request.user.username[:3]}{random_str}'

    order = Order.objects.create(order_id = order_id, user = request.user, package=package, food_price = food_price, accommodation_price = accommodation_price, total_price = total_price, created_at = today)
   
    context = {'user': cart.user, 'package':package, 'food': food, 'accommodation': accommodation, 'duration': package.duration, 'total_price': cart.total_price, 'order': order }
    
    return render(request, 'ticket.html', context)

def manager_dashboard(request):
    package = Package.objects.get(manager=request.user)
    tourists = Order.objects.filter(package = package)
    return render(request, 'manager_dashboard.html', {'package': package, 'tourists': tourists})


def orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders.html", {'orders': orders})

def cancel_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    can_cancel = 0
    if(order.package.start_date > date.today()):
        can_cancel = 1
    
    if request.method == 'POST':
        order.delete()
        return redirect('orders')
    print(can_cancel)
    return render(request, 'cancel_order.html', {'can_cancel': can_cancel, 'order': order})