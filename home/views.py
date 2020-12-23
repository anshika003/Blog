from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import post
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# html pages
def home(request):
    
    return render(request, 'home/home.html')

    
def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method== 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name,email,phone,content)
        if len(name)<4 or len(email)<10 or len(phone)<10 or len(content)<5:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,"Your message has been sent!")

    return render(request, 'home/contact.html')

 

def search(request):
    query = request.GET['query']
    if len(query)>70:
        allposts = post.objects.none()
    #allposts =post.objects.all() 
    else:

        allpostsTitle = post.objects.filter(title__icontains=query)
        allpostsContent = post.objects.filter(content__icontains=query)

        allposts = allpostsTitle.union(allpostsContent)
    if allposts.count == 0:
    
        messages.warning(request, "No search results found, please refine your query")


    params = {'allposts': allposts, 'query':query}

    return render(request, 'home/search.html', params)
 

#authentication APIS
def handleSignup(request):
    if request.method == 'POST':
            # Get the post parameters
        username = request.POST['username']
        fname= request.POST['fname']
        lname = request.POST['lname']
        email= request.POST['email']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']

           #check for erroneous input
        if  len(username) > 15:
            messages.error(request, "username must be under 15 characters")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "username should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('home')


            #create user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect('home')


    else:
        return HttpResponse('404-Not Found!')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, Please try again!")
            return redirect('home')
    return HttpResponse('404-Not Found!')


def handleLogout(request):
    
    logout(request)
    messages.success(request, "Successfully Logged Out!")
    return redirect('home')
    