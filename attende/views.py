from twilio.rest import Client
import os
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Employee, Travel, OnSite
import datetime
import re

def whatsapp(request):
    current_time = datetime.datetime.now()
    with open('data.json') as json_file:
        data = json.load(json_file)
    account_sid = 'ACa78997dd4d15c940e985159d6e503fa1'
    auth_token = '6d996929c5fe90cd904a2ace08326482'
    client = Client(account_sid, auth_token)
    bdy = []

    def listToString(s):
        str1 = ""
        for ele in s:
            str1 += ele
            str1 += "\n"
    # return string
        return str1
    try:
        z = []
        photoNamesList = []
        a = []
        with open('TravelImages.txt', 'r') as f:
            a = json.loads(f.read())
        for i in data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]:
            emp = Employee.objects.get(employee_phone=i[3:])
            name = emp.employee_name
            z.append(name)
            z.append("Employee_phone : " + " " + i)
            photo_name = data['Users']['attendance']['travelling'][str(
                current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['photo']
            if photo_name in a:
                print("Already sent")
            else:
                for k in data['Users']['attendance']['travelling'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]:
                    z.append(k + ":" + " " + str(data['Users']['attendance']['travelling'][str(
                        current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i][k]))
                    msg = listToString(z)
                message = client.messages.create(
                    media_url=[
                        f'https://snpc.code-e-python.com/media/attende/travel/{photo_name}'],
                    from_='whatsapp:+14155238886',
                    body=msg,
                    to='whatsapp:+917054394051'
                )
                z.clear()
                photoNamesList.append(photo_name)
                with open('TravelImages.txt', 'w') as f:
                    f.write(json.dumps(photoNamesList))
    except:
        print("Too many msgs resend again for remaining travelling details")
    try:
        y = []
        videoNamesList = []
        b = []
        with open('OnsiteVideo.txt', 'r') as f:
            b = json.loads(f.read())
        for i in data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))]:
            emp = Employee.objects.get(employee_phone=i[3:])
            name = emp.employee_name
            y.append(name)
            y.append("Employee_phone : " + " " + i)
            video_name = data['Users']['attendance']['on_site'][str(
                current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]['video']
            if video_name in b:
                print("Already sent")
            else:
                download_blob2(video_name)
                for k in data['Users']['attendance']['on_site'][str(current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i]:
                    y.append(k + ":" + " " + str(data['Users']['attendance']['on_site'][str(
                        current_time.year)][str(current_time.strftime("%m"))][str(current_time.strftime("%d"))][i][k]))
                msg2 = listToString(y)
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=msg2,
                    to='whatsapp:+917054394051'
                )
                message = client.messages.create(
                    media_url=[
                        f'https://snpc.code-e-python.com/media/attende/on_site/{video_name}'],
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+917054394051'
                )
                y.clear()
                videoNamesList.append(video_name)
                with open('OnsiteVideo.txt', 'w') as f:
                    f.write(json.dumps(videoNamesList))
                video_name = ""
                try:
                    audio_name = i+"_"+str(current_time.year)+"_" + \
                        str(current_time.strftime("%m"))+"_" + \
                        str(current_time.strftime("%d"))+"_"+"parts"+".mp3"
                    download_blobaudio(audio_name)
                    print(audio_name)
                    message = client.messages.create(
                        media_url=[
                            f'https://snpc.code-e-python.com/media/attende/onsiteaudios/{audio_name}'],
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+917054394051'
                    )
                except:
                    print("No parts audio")

                try:
                    audio_name1 = i+"_"+str(current_time.year)+"_" + \
                        str(current_time.strftime("%m"))+"_" + \
                        str(current_time.strftime("%d"))+"_"+"reasons"+".mp3"
                    download_blobaudio(audio_name1)
                    message = client.messages.create(
                        media_url=[
                            f'https://snpc.code-e-python.com/media/attende/onsiteaudios/{audio_name1}'],
                        from_='whatsapp:+14155238886',
                        to='whatsapp:+917054394051'
                    )
                except:
                    print("No reasons audio")

                print(audio_name)

    except:
        print("Too many on_site msgs")

    messages.success(request, "Your message has been sent")
    return redirect('/hd')

# Create your views here.


def signIn(request):
    if request.user.is_authenticated:
        return redirect('/hd')
    else:
        return render(request, 'attende/signIn.html')


def ad(request, st, id):
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
    a = Employee.objects.filter(emp_id=id).values(
        'employee_phone')[0]['employee_phone']
    uref = ref.child("+91"+str(a))
    uref.update({
        'status': int(st)
    })
    if request.method == "POST":
        d1 = request.POST['datefrom']
        d2 = request.POST['dateto']
        empwrkt = Travel.objects.filter(
            employee__emp_id=id, emp_date__range=(d1, d2))
        empwrkds = OnSite.objects.filter(
            employee__emp_id=id, emp_date__range=(d1, d2))
        params = {'empData': empData,
                  'empdetail': ed,
                  'totalemp': totalemp,
                  'empwrkt': empwrkt,
                  'empwrkds': empwrkds,
                  'id': id,
                  'd1': d1,
                  'd2': d2,
                  'totalemp': totalemp,
                  'os': onsiteEmployee,
                  'te': travelEmployee,
                  'inac': inactive}
        return render(request, 'attende/admin.html', params)
    else:
        params = {'empData': empData,
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
                  'inac': inactive}
        return render(request, 'attende/admin.html', params)


def hd(request):
    if request.user.is_authenticated:
        empData = []
        employe = Employee.objects.all()
        totalemp = Employee.objects.all().count()
        current_time = datetime.datetime.now()
        onsiteEmployee = OnSite.objects.filter(emp_date=current_time).count()
        travelEmployee = Travel.objects.filter(emp_date=current_time).count()
        inactive = totalemp - (onsiteEmployee+travelEmployee)
        for em in employe:
            empData.append(em)
        params = {'empData': empData,
                  'totalemp': totalemp,
                  'os': onsiteEmployee,
                  'te': travelEmployee,
                  'inac': inactive,
                  }
        return render(request, 'attende/admin.html', params)
    else:
        return redirect('/')


def addEmployee(request):
    ref = db.reference('/Users/profile_info')
    if request.method == "POST":
        name = request.POST['name2']
        phone = request.POST['phn2']
        designation = request.POST['desg2']
        email2 = request.POST['email2']
        aadhar = request.FILES['adhr2']
        adhrn = request.POST['adhrn']
        if Employee.objects.filter(employee_phone=phone).count() == 0:
            emp = Employee(employee_name=name, employee_phone=phone,
                           employee_email=email2, designation=designation, employee_aadhar=aadhar, employee_aadharNumber=adhrn)
            emp.save()
            messages.success(request, "Employee Added Succesfully !")
            uref = ref.child("+91"+phone)
            uref.update({
                'name': name,
                'email_id': email2,
                'phone_number': phone,
                'aadhaar_number': adhrn,
                'status': 1
            })
            a = Employee.objects.filter(employee_phone=phone).values(
                'employee_aadhar')[0]['employee_aadhar']
            img_name = a.split('/')[-1]
            upload_blob(img_name)
            return redirect('/hd')
        else:
            messages.warning(
                request, "User already added using this phone number")
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
            return redirect('/hd')
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
        employeeworkingdates = len(eval(Employee.objects.filter(emp_id=id).values(
            'employee_workingDates')[0]['employee_workingDates']))
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
            empwrkt = Travel.objects.filter(
                employee__emp_id=id, emp_date__range=(d1, d2))
            empwrkds = OnSite.objects.filter(
                employee__emp_id=id, emp_date__range=(d1, d2))
            params = {'empData': empData,
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
            params = {'empData': empData,
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
    if request.user.is_authenticated:
        empData = []
        employe = Employee.objects.all()
        for em in employe:
            empData.append(em)
        ed = Employee.objects.filter(emp_id=id)
        employeeworkingdates = len(eval(Employee.objects.filter(emp_id=id).values(
            'employee_workingDates')[0]['employee_workingDates']))
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
            empwrkt = Travel.objects.filter(
                employee__emp_id=id, emp_date__range=(d1, d2))
            empwrkds = OnSite.objects.filter(
                employee__emp_id=id, emp_date__range=(d1, d2))
            params = {'empData': empData,
                      'empdetail': ed,
                      'totalemp': totalemp,
                      'empwrkt': empwrkt,
                      'empwrkds': empwrkds,
                      'id': id,
                      'd1': d1,
                      'd2': d2,
                      'totalemp': totalemp,
                      'os': onsiteEmployee,
                      'te': travelEmployee,
                      'inac': inactive,
                      'count': employeeworkingdates}
            return render(request, 'attende/admin.html', params)
        else:
            params = {'empData': empData,
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
                      'inac': inactive,
                      'count': employeeworkingdates}
            return render(request, 'attende/admin.html', params)
    else:
        return redirect('/')


def search(request):
    query = request.GET['query']
    searchData = Employee.objects.filter(
        employee_name__icontains=query) or Employee.objects.filter(employee_phone__icontains=query)
    params = {'searchData': searchData}
    return render(request, 'attende/SearchPage.html', params)


def mapview(request, lat, long):
    params = {'la': lat,
              'lo': long}
    return render(request, 'attende/mapview.html', params)
