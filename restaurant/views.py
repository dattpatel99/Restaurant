from django.shortcuts import render
from math import ceil
from django.shortcuts import HttpResponse as http
from django.contrib.auth.models import User 
from restaurant.models import SignUp, CartItem, Item
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

# Functions to use in multiple places
def getItemsList(allItems):

    # Creates a list of dictionaries with catergory and itemName as key and the cats and names as value
    categoriesOfProducts = Item.objects.values('category', 'itemName')
    
    # Creates a set 
    # From the previous list takes only categories and creates a set of only categories
    categories = {i['category'] for i in categoriesOfProducts}

    # loops through the categories set and selects each category
    for cat in categories:
        # Filters the food item based on the category
        food = Item.objects.filter(category = cat)

        # Gets the number of food items in that category
        numItems = len(food)

        # creates nSlides for that food item
        if (numItems > 3):
            if (numItems // 3 == 0):
                nSlides = numItems / 3
            else:
                nSlides = ceil(numItems / 3)
        else:
            nSlides = 1

        # adds its to all items
        # Creates a list inside of the list allItems. The inner list holds: A query set of food type Item, followed by a range and then number of slide 
        allItems.append([food, range(1, nSlides), nSlides])



# Create your views here.
def home(request):
   
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')
'''
Works but add the prices
'''
def menu(request):
    items = []

    getItemsList(items)

    context = {'allItems': items}

    return render(request, 'menu.html', context)
'''
Works but add the prices
'''
def order(request):

    # in the event the usre is smart and enter /order/ in the url section
    if not request.user.is_authenticated:
        messages.info(request, "Please login or signup before trying to order.")
        return render(request, "login.html")

    # Learned from: CodeWithHarry
    # Credit: https://www.youtube.com/watch?v=6iDW97emfB0&list=PL1PPKISJVChyleKhFnRBWeYvBGElatze-&index=15&t=31s
    
    theItems = []

    getItemsList(theItems)
    
    context = {"allItems": theItems}
    
    return render(request, 'order.html', context)

'''
POST request not being sent
'''
def checkout(request):
    if request.method=="POST":
        print("I can see the post")
        itemsJSON = request.POST.get('itemsJson', '')
        print("Hello")
        order = CartItem(user = request.user, items_list = itemsJSON, order_date = datetime.now())
        print("Here")
        order.save()
        print("PAssed")
    return render (request, 'checkout.html')

'''
Works
Logs in user, if user entry wrong outputs error message
'''
def login(request):
    
    error = ""
    
    if request.method == "POST":
        # Gets users input for each field
        userMail = request.POST.get('inputedEmail')
        userPass = request.POST.get('inputedPassword')
        user = authenticate(request, username=userMail, password=userPass)
        # if there is a user of such then logs them in and renders the home page
    
        if user is not None:
            dj_login(request, user)
            error = "no"
            return render(request, "home.html")
        # Using elif because when redirecting from /order then message is show cased twice
        # otherwise changes the error var to yes
    
        elif user is None:
            error = "yes"
            messages.warning(request, "Invalid username or password. Try again.")
    
    context = {'error': error}

    return render(request, "login.html", context)


'''
Works
Signs up user 
'''
def signup(request):
    if request.method == "POST":
        # Basically gets all the form data field entries
        firstName=request.POST.get('firstName')
        lastName=request.POST.get('lastName')
        emailID=request.POST.get('email')
        number=request.POST.get('phone_num')
        address = request.POST.get('address')
        password=request.POST.get('password')
        
        # Creates new objects of newUser and singup 
        newUser = User.objects.create_user(username=emailID, password=password, first_name=firstName, last_name = lastName, date_joined = datetime.now())
        newUser.save()
        signup = SignUp.objects.create(user=newUser, phoneNum =number, address=address) 

    return render(request, 'newUser.html')

'''
Works
Logs out user and sends them to login page
'''
def logout(request):
    dj_logout(request)
    return render(request, "login.html")