from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee, WorkDates
import datetime
import re    
from firebase import Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

config = {
  "apiKey": "AIzaSyD4jECMBq3j9bSj9eYrjiOmDMLAQ3KxFRc",
  "authDomain": "snpc-attendence.firebaseapp.com/",
  "databaseURL": "https://snpc-attendence.firebaseio.com/",
  "storageBucket": "snpc-attendence.appspot.com",
  "serviceAccount": "snpc-attendence-firebase-adminsdk-ssdhp-541121d9ef.json"
}

firebase = Firebase(config)
cred = credentials.Certificate('snpc-attendence-firebase-adminsdk-ssdhp-541121d9ef.json')

firebase_admin.initialize_app(cred, {
        'databaseURL': "https://snpc-attendence.firebaseio.com/",
    })


def sync(request):
    ref = db.reference('/')
    userjson = ref.get()
    print(userjson)
    messages.success(request, "Data synced")
    return redirect('/hd')

# Create your views here.
def signIn(request):
    return render(request, 'attende/signIn.html')


def hd(request):
    if request.user.is_authenticated :
        empData = []
        employe = Employee.objects.all()
        for em in employe:
            empData.append(em)   
        totalemp = Employee.objects.all().count()      
        params = { 'empData' : empData,
                    'totalemp': totalemp }  
        return render(request, 'attende/admin.html', params)    
    else :
      return redirect('/')        


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
              return redirect( '/hd')
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
        return redirect('/hd')
    else:
        messages.error(request, "Invalid Credential")
        return redirect('/')

def handleLogout(request):
    logout(request)
    messages.success(request, "You are Logged Out !")
    return redirect('/')

def wd(request, id, date):
    if request.user.is_authenticated:
        empData = []
        employe = Employee.objects.all()
        for em in employe:
            empData.append(em)     
        ed = Employee.objects.filter(emp_id=id) 
        totalemp  = Employee.objects.all().count()  
        emplc = WorkDates.objects.filter(employee__emp_id=id, emp_date=date)
        empworkdt = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="Travel", emp_date=date) 
        empworkds = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="On Site", emp_date=date)
        if request.method == "POST":
            d1 = request.POST['datefrom']
            d2 = request.POST['dateto']
            empwrkt =  WorkDates.objects.filter(employee__emp_id=id, emp_work_status="Travel", emp_date__range=(d1, d2)) 
            empwrkds = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="On Site", emp_date__range=(d1, d2))  
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empwrkt': empwrkt,
                   'empwrkds': empwrkds,
                   'id': id,
                   'emplc': emplc,
                   'd1': d1,
                   'd2': d2}  
            return render(request, 'attende/admin.html', params)   
        else:
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empworkdt': empworkdt,
                   'empworkds': empworkds,
                   'id': id,
                   'emplc':emplc,
                   'd1': "mm-dd-yyyy",
                    'd2': "mm-dd-yyyy" }      
            return render(request, 'attende/admin.html', params) 
    else:
        messages.warning(request, "Something went wrong")
        return redirect('/hd')   



def homeadmin(request, id):
    if request.user.is_authenticated :
        empData = []
        employe = Employee.objects.all()
        for em in employe:
            empData.append(em)     
        ed = Employee.objects.filter(emp_id=id) 
        totalemp  = Employee.objects.all().count()  
        empworkdt = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="Travel") 
        empworkds = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="On Site")
        if request.method == "POST":
            d1 = request.POST['datefrom']
            d2 = request.POST['dateto']
            empwrkt =  WorkDates.objects.filter(employee__emp_id=id, emp_work_status="Travel", emp_date__range=(d1, d2)) 
            empwrkds = WorkDates.objects.filter(employee__emp_id=id, emp_work_status="On Site", emp_date__range=(d1, d2))  
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empwrkt': empwrkt,
                   'empwrkds': empwrkds,
                   'id': id ,
                    'd1': d1,
                    'd2': d2 }  
            return render(request, 'attende/admin.html', params)   
        else:
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empworkdt': empworkdt,
                   'empworkds': empworkds,
                   'id': id,
                   'd1': "mm-dd-yyyy",
                   'd2': "mm-dd-yyyy" } 
            return render(request, 'attende/admin.html', params) 
    else :
      return redirect('/')  


def search(request):
    query = request.GET['query']
    searchData = Employee.objects.filter(employee_name__icontains=query)
    params = {'searchData': searchData}
    return render(request, 'attende/SearchPage.html', params)     
