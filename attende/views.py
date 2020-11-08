from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee, Travel, OnSite
import datetime
import re    
from firebase import Firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

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
    with open('data.json','w') as f:
        json.dump(userjson,f)
    messages.success(request, "Data synced")
    with open('data.json') as json_file: 
      data = json.load(json_file) 
    def getList(dict):
        return dict.keys()
    d = getList(data['Users']['profile_info'])
    c = []
    for i in d:
        c.append(i)
    c.pop()    
    for emp in c:
        if Employee.objects.filter(employee_phone=data['Users']['profile_info'][emp]['phone_number']).count() == 0:
            emp = Employee(employee_name=data['Users']['profile_info'][emp]['name'], employee_email=data['Users']['profile_info'][emp]['email_id'],employee_phone=data['Users']['profile_info'][emp]['phone_number'])
            emp.save() 
        else:
            continue 
    current_time = datetime.datetime.now()   
    try:
        e = getList(data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))])
        f = []
        for i in e:
            f.append(i)
        f.pop()
        for i in f:
            a = getList(data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i])
        attendanceDetails = []
        for i in a:
            attendanceDetails.append(i)
        for i in f:
            if OnSite.objects.filter(employee=Employee.objects.get(employee_phone=i), emp_date=current_time).count() == 0:
                onsite = OnSite(employee=Employee.objects.get(employee_phone=i),emp_date=current_time,emp_latitude=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['current_location']['lat'],emp_longitude=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['current_location']['long'],emp_work_modelNumber=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['model_number'],emp_maintainParts=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['parts'],emp_partsReason=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['reason'],emp_totalProdution=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['total_production'],emp_siteInfo=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['site_info'],emp_running=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['total_run'])
                onsite.save()
            else:
                continue 
    except:
        print("no attendance on-site")
    try:
        g = getList(data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))])
        h = []
        for i in g:
            h.append(i)
        h.pop()
        for i in h:
            if Travel.objects.filter(employee=Employee.objects.get(employee_phone=i),emp_date=current_time).count() == 0:
                accList = []
                accList = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['total_workforce']
                trvl = Travel(employee=Employee.objects.get(employee_phone=i),emp_date=current_time,emp_latitudec=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['current_location']['lat'],emp_longitudec=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['current_location']['long'],travel_from=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['from'],travel_to=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['to'],travel_duration=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['duration'],travel_purpose=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['purpose'],emp_latitude1=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location1']['lat'],emp_longitude1=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location1']['long'],emp_latitude2=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location2']['lat'],emp_longitude2=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location2']['long'],emp_latitude3=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location3']['lat'],emp_longitude3=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['travelling_location']['location3']['long'],travel_by=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['transport'],accompanied_emp2=accList[0],accompanied_emp3=accList[1])  
                trvl.save()
            else:
                continue  
    except:
        print("No travelling details on this date")
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
        emplcS = OnSite.objects.filter(employee__emp_id=id, emp_date=date)
        emplcT = Travel.objects.filter(employee__emp_id=id, emp_date=date)
        empworkdt = Travel.objects.filter(employee__emp_id=id, emp_date=date) 
        empworkds = OnSite.objects.filter(employee__emp_id=id, emp_date=date)
        if request.method == "POST":
            d1 = request.POST['datefrom']
            d2 = request.POST['dateto']
            empwrkt =  Travel.objects.filter(employee__emp_id=id, emp_date__range=(d1, d2)) 
            empwrkds = OnSite.objects.filter(employee__emp_id=id, emp_date__range=(d1, d2))  
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empwrkt': empwrkt,
                   'empwrkds': empwrkds,
                   'id': id,
                   'emplcS': emplcS,
                   'emplcT': emplcT,
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
                   'emplcS': emplcS,
                   'emplcT': emplcT,
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
        empworkdt = Travel.objects.filter(employee__emp_id=id) 
        empworkds = OnSite.objects.filter(employee__emp_id=id)
        if request.method == "POST":
            d1 = request.POST['datefrom']
            d2 = request.POST['dateto']
            empwrkt =  Travel.objects.filter(employee__emp_id=id, emp_date__range=(d1, d2)) 
            empwrkds = OnSite.objects.filter(employee__emp_id=id, emp_date__range=(d1, d2))  
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
