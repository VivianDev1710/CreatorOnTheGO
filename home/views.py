from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import is_valid_path
from .forms import UploadForm
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Video, Text
from django.contrib.auth.forms import UserCreationForm
from .changes import editVideo
from .newCaptions import genNewCaption
import cv2
# Create your views here.

def index(request):
    username = None
    if request.user.is_anonymous:
        return redirect("/home/editor")
        # username = request.user.username
    vid_list = Video.objects.filter(user=request.user.get_username()).values()
    print("hello",vid_list,request.user.get_username(),type(vid_list))
    return render(request,"hello.html",{'videos':vid_list})
    # return render(request,'hello.html',{'user':username, 'videos':vid_list})

def about(request):
    return render(request,'about.html')
def caption(request):
    return redirect("/home/editor")

def generateCaption(request,videoid):
    print("yaha tak ho raha haii")
    vid= Video.objects.filter(id=videoid).values()
    cap=genNewCaption(vid[0].get("video"),request)
    print(cap)
    vid.update(caption=cap)
    return redirect("/home/editor/"+str(videoid))

@ensure_csrf_cookie
def editor(request):
    # if request.method=='POST':
    #     form=UploadFileForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         file = request.FILES['file']
    #         #print(file.name)
    #         handle_uploaded_file(file)
    #         return render(request, "editor.html", {'filename': file.name})
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload-display-video.html', {'form': form})
    if request.method=='POST':
        file=request.FILES.get('file')
        user=request.user.get_username()
        cap=str(request.FILES.get('file'))
        video=Video(video=file,user=user,caption=cap)
        video.save()
        # form=UploadForm(request.POST,request.FILES)
        # print("hello",request.POST)
        # if form.is_valid():
        #     form.save()
        return redirect("/home/main/")
    # else:
    #     form=UploadForm()
    return render(request,'editor.html')

def user(request):
    return render(request,'user.html')
def login_page(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print("hello",username,password)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            vid_list = Video.objects.filter(user=request.user.get_username()).values()
            print("hello",vid_list,request.user.get_username(),type(vid_list))
            return render(request,"hello.html",{'user':user,'videos':vid_list})
        else:
            return render(request,"login.html",{'login_fail':True})
    
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        email=request.POST.get("email")
        name=request.POST.get("name")
        password=request.POST.get("password")
        password2=request.POST.get("password2")
        if(password==password2):
            user=User(username=name,password=password,email=email)
            user.save()
            return render(request,"login.html",{'from_signup':True})
        else:
            return render(request,'signup.html',{'pass_miss_error':True})

        # user_form=UserCreationForm(request.POST)
        # if user_form.is_valid():
        #     user.form_save()
        #     return HttpResponse("<h1>Registration Success</h1>")
    # else:
    #     user_form=UserCreationForm()
            
    return render(request,'signup.html')

def logout_us(request):
    logout(request)
    return redirect("/home/main/")

def videoEditor(request,videoid):
    vid= Video.objects.filter(id=videoid).values()
    texts= Text.objects.filter(videoid=videoid).values()
    print("itne text hai", len(texts))
    from_time=vid[0].get("from_time")
    to_time=vid[0].get("to_time")
    cap = cv2.VideoCapture('C:/Users/Admin/Desktop/Semester 5/Software Eng/harry/media/video/22/'+vid[0].get("video")[9:])
    width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )
    w=int(height*(1080/1920))
    crop_max=width-w
    if from_time==-1:
        from_time="START"
        to_time="END"
    if request.method=="POST":
        # print("hellooozzzz",vid,request.POST)
        # Video.objects.filter(id=videoid)
        if request.POST.get("from")!="" and request.POST.get("to")!="":
            from_time=int(request.POST.get("from"))
            to_time=int(request.POST.get("to"))
            vid.update(from_time=int(request.POST.get("from")),to_time=int(request.POST.get("to")))
            
        vid.update(edited=True, filter=int(request.POST.get("filter")))
        editVideo(vid[0],request)
        # print(vid[0].get("video"))
    return render(request,'videoEditor.html',{'vid':vid[0],'video':vid[0].get("video")[9:-4],'from':from_time,'to':to_time,'crop_max':str(crop_max), 'texts':texts})

def addText(request,videoid):
    if request.method=='POST':
        textid= len(Text.objects.values())
        text=request.POST.get("text")
        from_time=request.POST.get("fromText")
        to_time=request.POST.get("toText")
        bg=request.POST.get("bgColor")
        fg=request.POST.get("fgColor")
        newText=Text.objects.create(textid=textid,text=text,videoid=videoid,from_time=from_time,to_time=to_time,bgColor="#f0f0f0",textColor="#0f0f0f")
        # newText=Text (textid=textid,text=text,videoid=videoid)
        print("This is text id:",newText.textid)
        newText.save()
        return redirect("/home/editor/"+str(videoid))

def deleteText(request,textid):
    print(Text.objects.filter(textid=textid)[0])
    videoid=Text.objects.filter(textid=textid)[0].videoid
    Text.objects.filter(textid=textid).delete()
    return redirect("/home/editor/"+str(videoid))

# @ensure_csrf_cookie
# def upload_display_video(request):
    
#     return render(request,'')
    # if request.method=='POST':
    #     form=UploadFileForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         file = request.FILES['file']
    #         #print(file.name)
    #         handle_uploaded_file(file)
    #         return render(request, "upload-display-video.html", {'filename': file.name})
    # else:
    #     form = UploadFileForm()
    # return render(request, 'upload-display-video.html', {'form': form})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

