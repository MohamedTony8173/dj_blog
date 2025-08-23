import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import Group
from accounts.models import CustomUser

from .forms import LoginForm, RegistrationUserForm


# Create your views here.
def register_account(request):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data["password"]
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password = password
            )
            user.save()
            
            
            current_domain = get_current_site(request).domain
            subject = 'activated an account'
            body = render_to_string('accounts/email_activate.html',{
                'user':user,
                'domain':current_domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user)
            })
            send_email = EmailMessage(subject=subject,body=body,to=[user.email],from_email='admin@site.com')
            send_email.send()
            messages.success(request,'please check you email address')
            return redirect('blog:home') 
    else:
        form = RegistrationUserForm(request.POST)  
    context = {
        'form':form
    }    
    return render(request,'accounts/register_accounts.html',context)


def active_account(request,uidb64,token):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = CustomUser.objects.get(id=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'You Can Log in Now')
        return redirect('accounts:login_account')
    else:
        messages.error(request,'invalid link was given ')
        return redirect('accounts:register_account')
        

def login_account(request):
    # if request.user.is_authenticated:
    #     messages.warning(request,'Do Not Play This Game! You are already Login :|(')
    #     return redirect('blog:home')
    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('blog:home')  # Replace 'home' with your desired redirect URL name
                else:
                    messages.error(request, 'Invalid email or password.')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login_account.html', {'form': form})


@login_required
def logout_account(request):
    logout(request)
    messages.success(request,'You Logged out')
    return redirect('blog:home')

def forget_password_account(request):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    
    return render(request,'accounts/forget_password.html')
        


def send_link_forget_password_account(request):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            current_domain = get_current_site(request).domain
            user = CustomUser.objects.get(email__exact=email)
            subject = 'forgot password'
            body = render_to_string('accounts/forgot_password_email.html',{
                'user':user,
                'domain':current_domain,
                'uid':urlsafe_base64_encode(force_bytes(user.id)),
                'token':default_token_generator.make_token(user)
            })
            send_email = EmailMessage(subject=subject,body=body,to=[email],from_email='admin@site.com')
            send_email.send()
            messages.success(request,'please check you email address')
            return redirect('blog:home') 
        else:
            messages.error(request, "no account with this is email has found")
            return redirect("accounts:forget_password_account")    
        
                
def reset_password_account(request,uidb64,token):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        user = CustomUser.objects.get(id=uid)
    except:
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session["uid"] = uid
        messages.success(request, "now you can reset your password safely")
        return redirect("accounts:final_reset_password")
    else:
        messages.error(request, "wrong link not appropriate")
        return redirect("accounts:login_account")

def final_reset_password(request):
    if request.user.is_authenticated:
        messages.warning(request,'Do Not Play This Game! You are already Login :|(')
        return redirect('blog:home')
    
    if request.method == 'POST':
        password = request.POST['password']    
        confirm_password = request.POST['confirm_password']  
        try:
            user = CustomUser.objects.get(id=request.session['uid'])  
            if password and not re.search(r'[A-Za-z]', password):  # checks for letters
                messages.error(request,"Password must contain at least one letter.")
                return redirect("accounts:final_reset_password")
        
            if password and not re.search(r'\d', password):  # checks for digits
                messages.error(request,"Password must contain at least one number.")
                return redirect("accounts:final_reset_password")
            
            if password and not re.search(r'[!@#$%^&*]', password):
                messages.error(request,"The password must contain at least one special character.")
                return redirect("accounts:final_reset_password")

            if password != confirm_password:
                messages.error(request,'password did not match')
                return redirect("accounts:final_reset_password")
            
            if password and len(password) < 6 :
                messages.error(request,'password length must be greater then {6} character')
                return redirect("accounts:final_reset_password")
                
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request,'your password has reset successfully !login now')
                return redirect("accounts:login_account")
        except:
            user = None
            messages.error(request, "Not reset password , some think goes wrong")
            return redirect("accounts:forget_password_account")
            
    return render(request, "accounts/password_reset.html")
                

                

                     