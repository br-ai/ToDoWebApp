from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Todo
from datetime import datetime, timedelta

def home(request):
    # send user to login page if he is not authentificated
    if request.user is None:
        return HttpResponseRedirect(reverse("login_view"))
    user = request.user
    todos = Todo.objects.filter(created_date__date = datetime.today().date(), user = user)

    # handle add todo function
    if request.method == 'POST':
        description = request.POST['description']
        heure_de_fin = request.POST['heure']
        current_time = datetime.now().strftime('%H:%M')
        
        
        try:
            # if hours is less than actual hours means that is for tomorrow
            if int(heure_de_fin[:2])<int(current_time[:2]):
                todo = Todo.objects.create(description = description, heure_de_fin = 'demain a '+heure_de_fin[:2]+'h'+heure_de_fin[2:], user = request.user)
                todo.save()
            else:
                todo = Todo.objects.create(description = description, heure_de_fin = 'a '+heure_de_fin[:2]+'h'+heure_de_fin[2:], user = request.user)
                todo.save()
            return render(request, 'index.html', {'todos':todos,})
        except Exception as e:
            return HttpResponse(e)
    else:
    
        return render(request, 'index.html', {'todos':todos,})

def historique(request):
    # display yestarday's stuff
    yesterday = datetime.now() - timedelta(1)
    user = request.user
    todos = Todo.objects.filter(created_date__date = yesterday, user = user)
    # handle form
    if request.method == 'POST':
        date = request.POST['date']
        dos = Todo.objects.filter(created_date__date = date, user = user)
        return render(request, 'historique.html', {'dos':dos, 'date':date})
        
    else:
        return render(request, 'historique.html', {'todos':todos,})

def creer_tache(request):
    if request.method == 'POST':
        description = request.POST['description']
        heure_de_fin = request.POST['heure']
        
        try:
            todo = Todo.objects.create(description = description, heure_de_fin = heure_de_fin)
            todo.save()
            return render(request, 'index.html', {})
        except Exception as e:
            return HttpResponse(e)
    return render(request, 'index.html', {})


def cloture(request):
    user = request.user
    todos = Todo.objects.filter(created_date__date = datetime.today().date(), user = user)
    todos_fait = Todo.objects.filter(created_date__date = datetime.today().date(), user = user, etat = True)
    todos_non_fait = Todo.objects.filter(created_date__date = datetime.today().date(), user = user, etat = False)
    
    return render(request, 'cloture.html', {'todos':todos, 'todos_fait':todos_fait, 'todos_non_fait':todos_non_fait, 'user':user})

@csrf_exempt
def changeState(request, id):
    if request.method == 'PUT':
        todo = Todo.objects.get(id = id)
        if todo.etat == True:
            todo.etat = False
            todo.save()
            return HttpResponse('201')
        else:
            todo.etat = True
            todo.save()
            return HttpResponse('201')
        
    return render(request, 'index.html', {})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["pass"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        
        # Ensure password matches confirmation
        password = request.POST["password1"]
        confirmation = request.POST["password2"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)    
            user.save()
            
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")
