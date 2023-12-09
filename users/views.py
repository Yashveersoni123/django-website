from email import message
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render, get_object_or_404
from dashboard.models import Article
from .utils import *
from django.contrib.auth.models import User
from.models import Profile, Comment, Contactus
import uuid
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from datetime import timedelta
from django.utils import timezone
import random
from django.contrib.sessions.models import Session



# Create your views here.
def index(request):
    data=Article.objects.all()
    paginator=Paginator(data, 6)
    page_number=request.GET.get('page')
    servicedatafinal=paginator.get_page(page_number)
    totalpage=servicedatafinal.paginator.num_pages
    return render(request, 'users/index.html', {
        "data":servicedatafinal, 
        "lastpage":totalpage, 
        "totalpagelist":[n+1 for n in range(totalpage)],
        "currentpage":servicedatafinal.number
        })


def single(request, content):
    article = get_object_or_404(Article, slug=content)
    totalarticles = Article.objects.all()
    comments = Comment.objects.filter(post_title=article).select_related('user')
    return render(request, 'users/single.html', {"data": article, "total": totalarticles, "comments":comments})

def search(request):
    query = request.GET.get('query', '')
    current_page = request.GET.get('currentpage', 1)  # Get the current page number

    article_list = Article.objects.filter(title__icontains=query)  # Filter by title

    paginator = Paginator(article_list, 10)  # 10 items per page
    articles = paginator.page(current_page)
   
    # If it's an AJAX request, return a JSON response
    article_data = []
    for article in articles:
        article_data.append({
            'title': article.title,
            'description': article.short_description,
            # Add more fields if needed
        })
        
        return JsonResponse({'articles': article_data})

    return render(request, 'search_results.html', {'articles': articles, 'query': query})

def contact(request):
    if request.method=="POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        message=request.POST.get('massage')
        data_obj=Contactus(name=fullname, email=email, massage=message)
        data_obj.save()
        return JsonResponse({'message': 'Message Sent'})

    return render(request, 'users/contact.html')

def sendcomment(request):
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        article_id = request.POST.get('article_id')
    
        try:
            article = Article.objects.get(slug=article_id)
            # Assuming 'user' is the logged-in user (adjust this according to your authentication)
            user = request.user  # Replace this with your user retrieval logic
            # Create a new comment
            comment = Comment.objects.create(post_title=article, comment=comment_text, user=user)
            # Return a success response
            return JsonResponse({'message': 'Comment submitted successfully'})
        except Article.DoesNotExist:
            return JsonResponse({'message': 'Article does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request'}, status=400)

def about (request):
    return render(request, 'users/about.html')


def editusername(request):
    if request.method=="POST":
        user_id=request.user.id
        user_obj=User.objects.get(id=user_id)
        user_obj.first_name=request.POST.get('firstname')
        user_obj.last_name=request.POST.get('lastname')
        user_obj.save()
    return redirect('/')


def verify(request, token):
    try:
        obj = Profile.objects.get(email_token=token)
        # Check if the token has expired
        if obj.token_expires_at < timezone.now():
            return HttpResponse("Token has expired.")
        # Set the user as verified
        obj.is_verified = True
        obj.save()
        # Create the user if not already created
        if not obj.user.is_active:
            obj.user.is_active = True
            obj.user.save()
            return redirect('home')
        
    except Profile.DoesNotExist:
        return HttpResponse("Invalid token")
    
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Check if the email already exists in the User model
        if User.objects.filter(email=email).exists():
            existing_user = User.objects.get(email=email)
            return JsonResponse({'message': False})
        # Create a new user
        user_obj = User.objects.create_user(email, email=email, password=password)
        user_obj.first_name = firstname
        user_obj.last_name = lastname
        user_obj.is_superuser = False  # Set the user as a superuser
        user_obj.is_staff = False 
        user_obj.is_active = False
        user_obj.save()
        # Create a related Profile for the user
        token_expiry = timezone.now() + timedelta(minutes=20)  # Calculate token expiry time (20 minutes)
        p_obj = Profile.objects.create(
            user=user_obj,
            email_token=str(uuid.uuid4()),
            token_expires_at=token_expiry  # Store token expiry time in the profile
        )
        send_email_token(email, p_obj.email_token)
        return JsonResponse({'message': True})
    
    return render(request, 'users/signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')  # Corrected to fetch the 'password' field
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': True})
        else:
            return  JsonResponse({'message': 'email and password is wrong'})
    
    return render(request, 'users/signin.html')

def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        length = 6
        characters = "0123456789"
        condition = request.POST.get('condition')
        otp = request.POST.get('otp')
        newpassword = request.POST.get('newpassword')
       
        print(email)
        print(condition)
        if condition == '1':  # Check if condition is a string '1', not an integer
            otp_generate = ''.join(random.choices(characters, k=length))
            request.session['otp_generate'] = otp_generate
            try:
                user = User.objects.get(email=email)
                send_otp_token(email, otp_generate)
                return JsonResponse({'message': 'OTP sent to the email'})
            except User.DoesNotExist:
                return JsonResponse({'message': True})  # No user found with this email
        else:
            otp_generate = request.session.get('otp_generate')
            if otp_generate==otp:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(newpassword)
                    user.save()
                    # Password updated successfully
                    return  JsonResponse({'message': True})  # Replace with your template name
                except User.DoesNotExist:
                    # User with this email does not exist
                    return HttpResponse("User with this email does not exist")  # Replace with your template name
            else:
                return JsonResponse({'message':2})
    
    return render(request, 'users/signin.html')




def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')


















