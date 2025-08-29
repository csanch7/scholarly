from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("completed", views.completedview, name="completedview"),
    

    # API Routes 
    path("scholarships", views.scholarships, name="scholarships"),
    path("scholarships/add", views.compose, name="compose"),
    path("scholarships/edit/<int:scholarship_id>", views.edit, name="edit"),
    path("scholarships/remove/<int:scholarship_id>", views.remove, name="remove"),
    path("scholarships/<int:scholarship_id>", views.scholarship, name="scholarship"),
    path("scholarships/recieved/<int:scholarship_id>", views.recievedScholarship, name="recievedScholarship"),
    path("scholarships/<int:scholarship_id>/adddocumentlink", views.adddocumentlink, name="adddocumentlink"),
    







]