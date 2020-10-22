
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name="signIn"),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handleLogin, name="handleLogIn"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('homeadmin/', views.homeadmin, name="homeadmin"),
    path('search/', views.search, name="search"),
    path('empDetails/<empId>', views.empDetails, name="empDetails")


]