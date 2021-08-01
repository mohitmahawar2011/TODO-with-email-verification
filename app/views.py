import uuid

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout, login
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from django.contrib.auth.models import User

from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


@login_required()
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos})

# def logining(request):
    # if request.method == 'GET':
    #     form1 = AuthenticationForm()
    #     context = {
    #         "form" : form1
    #     }
    #     return render(request , 'login.html' , context=context )
    # else:
    #     form = AuthenticationForm(data=request.POST)
    #     print(form.is_valid())
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username = username , password = password)
    #         if user is not None:
    #             loginUser(request , user)
    #             return redirect('home')
    #     else:
    #         context = {
    #             "form" : form
    #         }
    #         return render(request , 'login.html' , context=context )


# def signup(request):
#
#     if request.method == 'GET':
#         form = UserCreationForm()
#         context = {
#             "form" : form
#         }
#         return render(request , 'signup.html' , context=context)
#     else:
#         print(request.POST)
#         form = UserCreationForm(request.POST)
#         context = {
#             "form" : form
#         }
#         if form.is_valid():
#             user = form.save()
#             print(user)
#             if user is not None:
#                 return redirect('login')
#         else:
#             return render(request , 'signup.html' , context=context)



@login_required()
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})


def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')




# for email verified:--

def logining(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')

        profile_obj = TODO.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')

        login(request, user)

        return redirect('home')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/signup')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/signup')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = TODO.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)

            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'signup.html')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def verify(request, auth_token):
    try:
        profile_obj = TODO.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('home')


def token_send(request):
    return render(request , 'token_send.html')


def error_page(request):
    return render(request, 'error.html')