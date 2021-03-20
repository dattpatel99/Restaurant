from django.shortcuts import render
from django.shortcuts import HttpResponse as http
from django.contrib.auth.models import User 
from restaurant.models import SignUp
from restaurant.models import Items
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

# Create your views here.

def home(request):
   
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def menu(request):
    return render(request, 'menu.html')

@login_required
def order(request):
    items = Items.objects.all()
    context ={
        'items': items
    }
    return render(request, 'order.html', context)

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
        # otherwise changes the error var to yes
        else:
            error = "yes"
    context={'error':error}
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
