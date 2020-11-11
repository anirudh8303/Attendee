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
from firebase_admin import storage
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
                'storageBucket': 'snpc-attendence.appspot.com'
    
    })

#storage = firebase.storage() 
bucket = storage.bucket()   

def download_blob(source_file):
    bucket = storage.bucket()
    fname = source_file.split('.')
    blob = bucket.blob('Travel/'+fname[0])
    blob.download_to_filename('media/attende/travel/' + fname[0]+'.'+fname[1])
    print("Downloaded ", fname)
    return  fname[0]+'.'+fname[1]

def upload_blob(file_location):    
    bucket = storage.bucket()
    blob = bucket.blob('AadharCard/'+file_location)
    blob.upload_from_filename('./media/attende/aadhar/'+file_location)
    #fbase_location = 'gs://snpc-attendence.appspot.com/AadharCard' + fname
    print("Uploaded ", file_location)

def sync(request):
    current_time = datetime.datetime.now() 
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
        c.append(i[3:])
    c.pop()   
    for emp in c:
        if Employee.objects.filter(employee_phone=data['Users']['profile_info']["+91"+emp]['phone_number']).count() == 0:
            dates = data['Users']['profile_info']["+91"+emp]['attendance'][str(current_time.year)][str(current_time.strftime("%m"))]
            date_list = [x for x in dates]
            emp = Employee(employee_name=data['Users']['profile_info']["+91"+emp]['name'],employee_status=data['Users']['profile_info']["+91"+emp]['status'],employee_workingDates=date_list, employee_email=data['Users']['profile_info']["+91"+emp]['email_id'],employee_phone=data['Users']['profile_info']["+91"+emp]['phone_number'])
            emp.save() 
        else:
            continue 
        e = getList(data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))])
        f = []
        for i in e:
            f.append(i[3:])
        for i in f:
            try:
                if OnSite.objects.filter(employee=Employee.objects.get(employee_phone=i), emp_date=current_time).count() == 0:
                    onsite = OnSite(employee=Employee.objects.get(employee_phone=i),emp_date=current_time,emp_latitude=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['current_location']['lat'],emp_longitude=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['current_location']['long0'],emp_work_modelNumber=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['model_number'],emp_maintainParts=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['parts'],emp_partsReason=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['reason'],emp_totalProdution=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['total_production'],emp_siteInfo=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['site_info'],emp_running=data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['total_run'])
                    onsite.save()
                else:
                    continue 
            except:
                print("no data on-site for this user")    
    g = getList(data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))])
    h = []
    for i in g:
        h.append(i[3:])
    for i in h:
        try:
            if Travel.objects.filter(employee=Employee.objects.get(employee_phone=i),emp_date=current_time).count() == 0:
                trvl = Travel(employee=Employee.objects.get(employee_phone=i),travel_force=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['totalforce'], travel_Image=download_blob(data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['photo']), emp_date=current_time,emp_latitudec=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['current_location']['lat'],emp_longitudec=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['current_location']['long0'],travel_from=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['from'],travel_to=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['to'],travel_duration=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['duration'],travel_purpose=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['purpose'],travel_by=data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['transport'])  
                trvl.save()  
            else:
                continue   
        except:
            print("no data for user") 
    for i in h:
        try:
            trvle = Travel.objects.get(employee=Employee.objects.get(employee_phone=i))
            trvle.emp_latitude1 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location1']['lat'] 
            trvle.emp_longitude1 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location1']['long0'] 
            trvle.save()
            trvle.emp_latitude2 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location2']['lat'] 
            trvle.emp_longitude2 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location2']['long0'] 
            trvle.save()
            trvle.emp_latitude3 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location3']['lat'] 
            trvle.emp_longitude3 = data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]["+91"+i]['travelling_location']['location3']['long0'] 
            trvle.save()
        except:
            print("no travelling_ location data for user")        

    return redirect('/hd')

# Create your views here.
def signIn(request):
    if request.user.is_authenticated:
        return redirect('/hd')
    else:
        return render(request, 'attende/signIn.html')

def ad(request,st,id):
    ref = db.reference('/Users/profile_info/')
    e = Employee.objects.get(emp_id=id)
    e.employee_status = st
    e.save()
    empData = []
    employe = Employee.objects.all()
    for em in employe:
        empData.append(em)     
    ed = Employee.objects.filter(emp_id=id) 
    totalemp = Employee.objects.all().count()  
    current_time = datetime.datetime.now()
    onsiteEmployee = OnSite.objects.filter(emp_date=current_time).count()
    travelEmployee = Travel.objects.filter(emp_date=current_time).count()
    inactive = totalemp - (onsiteEmployee+travelEmployee)
    empworkdt = Travel.objects.filter(employee__emp_id=id) 
    empworkds = OnSite.objects.filter(employee__emp_id=id)
    a = Employee.objects.filter(emp_id=id).values('employee_phone')[0]['employee_phone']
    uref = ref.child("+91"+str(a))
    uref.update({
        'status': int(st)
        })
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
                    'd2': d2,
                    'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive }  
        return render(request, 'attende/admin.html', params)   
    else:
        params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empworkdt': empworkdt,
                   'empworkds': empworkds,
                   'id': id,
                   'd1': "mm-dd-yyyy",
                   'd2': "mm-dd-yyyy",
                   'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive } 
        return render(request, 'attende/admin.html', params) 


def hd(request):
    if request.user.is_authenticated :
        empData = []
        employe = Employee.objects.all()
        totalemp = Employee.objects.all().count()  
        current_time = datetime.datetime.now()
        onsiteEmployee = OnSite.objects.filter(emp_date=current_time).count()
        travelEmployee = Travel.objects.filter(emp_date=current_time).count()
        inactive = totalemp - (onsiteEmployee+travelEmployee)
        for em in employe:
            empData.append(em)       
        params = { 'empData' : empData,
                    'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive,
                     }  
        return render(request, 'attende/admin.html', params)    
    else :
      return redirect('/')        

def addEmployee(request):
    ref = db.reference('/Users/profile_info')
    if request.method == "POST":
        name = request.POST['name2']
        phone =  request.POST['phn2']
        designation = request.POST['desg2']
        email2 = request.POST['email2']
        aadhar =  request.FILES['adhr2']
        if Employee.objects.filter(employee_phone=phone).count() == 0:
            emp = Employee(employee_name=name, employee_phone=phone,employee_email=email2, designation=designation, employee_aadhar=aadhar)
            emp.save()
            messages.success(request, "Employee Added Succesfully !")
            uref = ref.child("+91"+phone)
            uref.update({
            'name': name,
            'email_id': email2,
            'phone_number': phone,
            'status': 1 
            })
            a = Employee.objects.filter(employee_phone=phone).values('employee_aadhar')[0]['employee_aadhar']
            img_name = a.split('/')[-1]
            upload_blob(img_name)
            return redirect( '/hd')
        else:
            messages.warning(request, "User already added using this phone number")
            return redirect('/hd')    
    else:
        return HttpResponse('404 NOT FOUND') 


def handleSignUp(request):
    if request.method == "POST":
        name = request.POST['name1']
        email1 = request.POST['email1']
        username = request.POST['username1']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 == pass2:
              myuser = User.objects.create_user(username, email1, pass1)
              myuser.first_name = name
              myuser.save()
              messages.success(request, "Admin Added Succesfully !")
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
        employeeworkingdates = len(eval(Employee.objects.filter(emp_id=id).values('employee_workingDates')[0]['employee_workingDates']))
        totalemp = Employee.objects.all().count()  
        current_time = datetime.datetime.now()
        onsiteEmployee = OnSite.objects.filter(emp_date=current_time).count()
        travelEmployee = Travel.objects.filter(emp_date=current_time).count()
        inactive = totalemp - (onsiteEmployee+travelEmployee)
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
                   'd2': d2,
                   'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive,
                    'count': employeeworkingdates}  
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
                    'd2': "mm-dd-yyyy",
                    'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive,
                    'count': employeeworkingdates}      
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
        totalemp = Employee.objects.all().count()  
        current_time = datetime.datetime.now()
        onsiteEmployee = OnSite.objects.filter(emp_date=current_time).count()
        travelEmployee = Travel.objects.filter(emp_date=current_time).count()
        inactive = totalemp - (onsiteEmployee+travelEmployee)
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
                    'd2': d2,
                    'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive }  
            return render(request, 'attende/admin.html', params)   
        else:
            params = { 'empData' : empData,
                   'empdetail': ed,
                   'totalemp': totalemp,
                   'empworkdt': empworkdt,
                   'empworkds': empworkds,
                   'id': id,
                   'd1': "mm-dd-yyyy",
                   'd2': "mm-dd-yyyy",
                   'totalemp': totalemp,
                    'os': onsiteEmployee,
                    'te': travelEmployee,
                    'inac': inactive } 
            return render(request, 'attende/admin.html', params) 
    else :
      return redirect('/')  


def search(request):
    query = request.GET['query']
    searchData = Employee.objects.filter(employee_name__icontains=query) or Employee.objects.filter(employee_phone__icontains=query)
    params = {'searchData': searchData}
    return render(request, 'attende/SearchPage.html', params)     
