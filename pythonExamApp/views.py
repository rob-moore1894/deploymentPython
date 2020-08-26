from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Quotes
from django.db.models import Q
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    regValidation = Users.objects.regValidator(request.POST)
    print(regValidation)
    if len(regValidation) > 0:
        for value in regValidation.values():
            messages.error(request, value)
        return redirect('/')
    else: 
        hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newUser = Users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashedPw)
        request.session['loggedInId'] = newUser.id
    return redirect('/quotes')

def login(request):
    loginValidation = Users.objects.loginValidator(request.POST)
    print(loginValidation)
    if len(loginValidation) > 0:
        for value in loginValidation.values():
            messages.error(request, value)
        return redirect('/')
    else: 
        usersByEmail = Users.objects.filter(email= request.POST['emailLogin'])
        request.session['loggedInId'] = usersByEmail[0].id
        return redirect('/quotes')

def quotesPage(request):
    context = {
        'loggedInUser': Users.objects.get(id=request.session['loggedInId']),
        'all_users': Users.objects.all(),
        'all_quotes': Quotes.objects.all(),
        'user_liked': Quotes.objects.filter(favoriters = Users.objects.get(id=request.session['loggedInId'])),
    }
    return render(request, "quotes.html", context)

def addQuote(request):
    quoteValidation = Users.objects.quoteValidator(request.POST)
    print(quoteValidation)
    if len(quoteValidation) > 0:
        for value in quoteValidation.values():
            messages.error(request, value)
        return redirect('/quotes')
    else: 
        this_user = Users.objects.get(id=request.session['loggedInId'])
        newQuote = Quotes.objects.create(author= request.POST['author'], content = request.POST['quote'], uploader=this_user)
    return redirect('/quotes')

def userPage(request, uploaderId):
    context = {
        'selectedUser': Users.objects.get(id=uploaderId),
        'user_quotes': Quotes.objects.filter(uploader=Users.objects.get(id=uploaderId))
    }
    return render(request, "user.html", context)

def addLike(request, quoteId):
    print(quoteId)
    user_liking = Users.objects.get(id=request.session["loggedInId"])
    quote_liked = Quotes.objects.get(id=quoteId)
    user_liking.quotes_favorited.add(quote_liked)
    return redirect('/quotes')

def editPage(request, userId):
    context = {
        'user': Users.objects.get(id=userId),
    }
    return render(request, "edit.html", context)

def updateUser(request):
    userId = request.session['loggedInId']
    thisUser = Users.objects.get(id=userId)
    updateValidation = Users.objects.updateValidator(request.POST)
    if len(updateValidation) > 0:
        for value in updateValidation.values():
            messages.error(request, value)
        return redirect(f'/myaccount/{userId}')
    else: 
        thisUser.first_name = request.POST['newFname']
        thisUser.last_name = request.POST['newLname']
        thisUser.email = request.POST['newEmail']
        thisUser.save()
    return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')