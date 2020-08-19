from django.shortcuts import render, HttpResponse, redirect
from blog.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def about(request):
    messages.info(request, 'Details Regarding Blog.')

    return render(request, 'home/about.html')

def contact(request):
    # messages.error(request, 'you may contact us by sharing your query with us.')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,"Please fill the form correctly")
        else:
            contact =  Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "your messages has been successfully sent")

    return render(request, 'home/contact.html')

def search(request):
    # allPosts = Post.objects.all()
    query = request.GET['query']
    if len(query)>78:
        allPosts =Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
        if allPosts.count() == 0:
            messages.warning(request,"No search results found.Please Fillup the right query")
        params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        #Get the post parameters
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check for enormous inputs
        #username checks
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')
        #under chac and no.checks
        if not username.isalnum():
            messages.error(request, "Username must be under letter, numbers")
            return redirect('home')
        #password checks
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')
        #create new user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request, "Your R|_|N MyBlog account has been successfully  created")
        return redirect('home')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        #Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect('home')
    return HttpResponse('handleLogin')
    return HttpResponse('404 - Not Found')

def handleLogout(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('home')
    return HttpResponse('handleLogout')


