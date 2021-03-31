from django.shortcuts import render
from django.core.mail import send_mail as Mail
from math import ceil
from django.shortcuts import HttpResponse as http
from django.contrib.auth.models import User 
from restaurant.models import CartItem, Item
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

# Functions to use in multiple places
def getItemsList(allItems):

    # Creates a list of dictionaries with catergory and itemName as key and the cats and names as value
    categoriesOfProducts = Item.objects.values('category', 'itemName', 'price')
    
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

# For making the order string easily readable
def changeOrder(theOrder):
    # Will hold the final string
    finalString = ""

    #Making the order easier to form into one string by removing some character
    theOrder = theOrder.replace("{", "")
    theOrder = theOrder.replace("}", "")
    theOrder = theOrder.replace('"', "")
    theOrder = theOrder.replace('"', "")

    # Splits the order to be 1 item as an element
    listOne = theOrder.split(",")
    for i in range(0, len(listOne)-1, 2):
        tempStr = listOne[i] + "|" + listOne[i+1]

        # Splits the single order into itemName and a string holding quantity and price
        lisSecond = tempStr.split(":")
        itemName = lisSecond[0]

        # Splits the string with quantity and price into a list of each as an element
        listThird = lisSecond[1].split("|")
        for j in range(0, len(listThird)):

            # Removes some useless characters from the quantity string and price
            listThird[j] =  listThird[j].replace("[","")
            listThird[j] = listThird[j].replace("]","")

            # Stores each 
            pricePerItem = listThird[1]
            quan = listThird[0]

        # Forms a final string
        finalString = finalString + itemName + " Quantity: " + quan + " Price per item: " + pricePerItem + " = " + str(int(quan) * float(pricePerItem)) + "\n"
    return finalString

# Create your views here.
'''
Works
The home page
'''
def home(request):
   
    return render(request, 'home.html')

'''
Works
Allows user to enter feedback
'''
def contact(request):
    if request.method == "POST":
        nameOfUser = request.POST.get("name")
        emailUser = request.POST.get("email")
        idOrder = request.POST.get("orderID")
        number = request.POST.get("phone")
        message = request.POST.get("message")

        # Email variables to use
        subject = "Customer Contact from " + nameOfUser
        emailMsg = "User email: " + emailUser + "\n\n Order ID: " + idOrder + "\n\n Message: " + message + "\n\n Phone Number: " + number
        emailRecevier = "flask.tutorial21@gmail.com"

        #Send email to admin whoever they are
        Mail(
            subject,
            emailMsg,
            request.user.username,
            [emailRecevier],
            fail_silently=False
        )
        emailSent = "Thank you for your feedback!"
        context = {'sent': 'yes', 'cusMsg' : emailSent}
    else:
        context = {'sent': 'no', 'cusMsg': 'null'}

    return render(request, 'contact.html', context)
'''
Works 
Shows the menu to user without them having to login
'''
def menu(request):
    items = []

    getItemsList(items)

    context = {'allItems': items}

    return render(request, 'menu.html', context)
'''
Works
Takes users order 
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
Works
Checks out the user
'''
def checkout(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login or signup before trying to order.")
        return render(request, "login.html")
    if request.method == "POST":
        order = request.POST.get("itemsJSON")
        order = changeOrder(order)
        orderCost = request.POST.get("orderCost")
        phone = request.POST.get("phone_num")
        address = request.POST.get("address")
        cart = CartItem(user=request.user, phoneNum=phone, address=address, cost=int(orderCost), list=order, order_date=datetime.now())
        cart.save()

        # So that we can send the order ID somehow
        newId = cart.orderId
        cart.string_id = str(newId)

        # Email variables to use
        subject = "New Order ID: " + cart.string_id
        emailMsg = "User = " + request.user.username + "\n\n" + order + "\n\n" + "Total cost: " + orderCost
        emailRecevier = "flask.tutorial21@gmail.com"


        #Send email to admin whoever they are
        Mail(
            subject,
            emailMsg,
            request.user.username,
            [emailRecevier],
            fail_silently=False
        )
       
        # Create thank you message to alert user
        msg = "Thank you for ordering! You order Id is:"
        id = cart.orderId
        context = {'id': id}
        messages.success(request, msg)
        
        # Redirect to home page
        return render(request, 'home.html', context)
    return render(request, 'checkout.html')

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
        password=request.POST.get('password')
        
        # Creates new objects of newUser and singup 
        newUser = User.objects.create_user(username=emailID, password=password, first_name=firstName, last_name = lastName, date_joined = datetime.now())
        newUser.save()

    return render(request, 'newUser.html')

'''
Works
Logs out user and sends them to login page
'''
def logout(request):
    dj_logout(request)
    return render(request, "login.html")