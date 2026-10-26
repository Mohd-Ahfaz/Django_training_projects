from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def Gotoempdashboard(Request):
    return render(Request, 'Empdashboard.html')

def Display(Request):
    pass
def Insertdata(Request):
    pass
def Updatedata(Request):
    pass
def Deletedata(Request):
    pass
def Signup(Request):
    if Request.method == 'POST':
        uname = Request.POST.get('uname')
        email = Request.POST.get('email')
        password = Request.POST.get('password')
        confirm_password = Request.POST.get('passwordagain')
        print(uname,email,password,confirm_password)
        if password != confirm_password:
            messages.error(Request,"Please Enter Similar Passwords") 
            return redirect('Signup')
    
        if User.objects.filter(username=uname).exists():
            messages.error(Request,"Username Already Exists") 
            return redirect('Signup') 
        
        if User.objects.filter(email=email).exists():
            messages.error(Request,"Email Already Exists")  
            return redirect('Signup')
   
        x = User.objects.create_user(username = uname, email = email, password = password) 
        print(x)
        login(Request,x)
        messages.success("Login Successful")   
        return redirect('index')  

     
    return render(Request, 'Signupform.html')

def Emplogin(Request):
    if Request.method == 'POST':
        unam= Request.POST.get('unam')
        pas = Request.POST.get('pas')
        print(unam,pas)
        x = authenticate(username = unam, password = pas)
        #create session ID
        
        Request.session['username']=unam
        print('session id-->',unam)
        if x is not None:
            login(Request,x)
            # 10 seconds
            Request.session.set_expiry(10)
            return redirect('Empd')
    return render(Request, 'Loginform.html')

def LLogout(Request):
    logout(Request)
    Request.session.flush()
    return redirect('index')
    