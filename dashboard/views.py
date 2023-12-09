from xmlrpc.client import DateTime
from django.shortcuts import render,HttpResponse, redirect, get_object_or_404, get_list_or_404
from .models import Article
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    data=Article.objects.all()
    paginator=Paginator(data, 10)
    page_number=request.GET.get('page')
    servicedatafinal=paginator.get_page(page_number)
    totalpage=servicedatafinal.paginator.num_pages
    return render(request, 'dashboard/index.html', {
        "data":servicedatafinal, 
        "lastpage":totalpage, 
        "totalpagelist":[n+1 for n in range(totalpage)],
        "currentpage":servicedatafinal.number
        })

def comment(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    return render(request, 'dashboard/comment.html')



def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    
    if request.method== "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            return redirect('dashboard:signin')
        
    return render(request, 'dashboard/signin.html')

def signout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('dashboard:dashboard')

def setting(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    return render(request, 'dashboard/setting.html')

def media(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    image=Article.objects.all()
    return render(request, 'dashboard/medialibrary.html', {'data':image})

def create(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    categories = Article.category_choice
    subcategories = Article.sub_category_choice
    return render(request, 'dashboard/create_post.html', {"categories": categories, "subcategories":subcategories})

def edit(request, data):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    original_string = data
    converted_string = original_string.replace('-', ' ')
    sl = get_object_or_404(Article, title=converted_string)
    if request.method == 'POST':
        sl.title = request.POST.get('Title')
        sl.img_title = request.POST.get('ImgTitle')
        sl.img_alt = request.POST.get('ImgALT')
        sl.tags = request.POST.get('Tags')
        sl.short_description = request.POST.get('Description')
        sl.main_content = request.POST.get('editordata')
        new_thumbnail = request.FILES.get('Thumbnail')
        if not sl.thumbnail and new_thumbnail:
            sl.thumbnail = new_thumbnail
        elif new_thumbnail:
            sl.thumbnail.delete() 
            sl.thumbnail = new_thumbnail

        sl.save()
    return render(request, 'dashboard/edit_post.html', {"data":sl})

def createPOST(request):
    if not request.user.is_authenticated:
        return redirect('dashboard:signin')
    if request.method == 'POST':
        title = request.POST.get('Title')
        imgtitle=request.POST.get('ImgTitle')
        slug=request.POST.get('Slug')
        imgalt=request.POST.get('ImgALT')
        tags=request.POST.get('Tags')
        thumbnail=request.FILES.get('Thumbnail')
        shortdescription=request.POST.get('Description')
        maincontent=request.POST.get('editordata')
        data=Article(title=title,img_title=imgtitle,slug=slug,img_alt=imgalt,tags=tags,thumbnail=thumbnail,short_description=shortdescription,main_content=maincontent)
        data.save()
        
        return redirect('dashboard:create')
    return HttpResponse("Invalid request")


