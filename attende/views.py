from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee
# Create your views here.
def signIn(request):
    return render(request, 'attende/signIn.html')


def handleSignUp(request):
    if request.method == "POST":
        name = request.POST['name1']
        phone =  request.POST['phn']
        location = request.POST['loc']
        designation = request.POST['desg']
        email1 = request.POST['email1']
        username = request.POST['username1']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        aadhar =  request.FILES['adhr']
        if pass1 == pass2:
              myuser = User.objects.create_user(username, email1, pass1)
              myuser.save()
              emp = Employee(employee_name=name, employee_phone=phone, employee_username=username, employee_email=email1, designation=designation, place=location, employee_aadhar=aadhar)
              emp.save()
              messages.success(request, "Employee Added Succesfully !")
              return redirect( '/homeadmin')
        else:
            messages.warning(request, "Passwords did not match !")
            return redirect('/')
    else:
        return HttpResponse('404-Not Found')





def handleLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "You are logged in !")
        return redirect('/homeadmin')
    else:
        messages.error(request, "Invalid Credential")
        return redirect('/')

def handleLogout(request):
    logout(request)
    messages.success(request, "You are Logged Out !")
    return redirect('/')


def homeadmin(request):
    if request.user.is_authenticated :
        empData = []
        employe = Employee.objects.all()
        for em in employe:
            empData.append(em)
        params = { 'empData' : empData}    
        return render(request, 'attende/admin.html', params)    
    else :
      return redirect('/')  


def search(request):
    query = request.GET['query']
    searchData = Employee.objects.filter(employee_name__icontains=query)
    params = {'searchData': searchData}
    return render(request, 'attende/SearchPage.html', params)     

def empDetails(request, empId):
    empD = Employee.objects.filter(emp_id=empId)
    params = {'empdetail': empD}
    return render(request, 'attende/empDetails.html', params)           
