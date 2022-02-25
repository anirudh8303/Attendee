from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name="signIn"),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handleLogin, name="handleLogIn"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('hd/', views.hd, name="hd"),
    path('homeadmin/<id>', views.homeadmin, name="homeadmin"),
    path('search/', views.search, name="search"),
    path('workdetail/<id>/<date>', views.wd, name="wd"),
    #path('sync/', views.sync, name="sync"),
    path('ad/<st>/<id>', views.ad, name="ad"),
    path('addemployee/', views.addEmployee, name="addEmployee"),
    path('mapview/<lat>/<long>', views.mapview, name="mapview"),
    path('sendonwhatsapp/', views.whatsapp, name="whatsapp")

]
