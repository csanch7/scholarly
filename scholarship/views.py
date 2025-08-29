import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django import forms
from django.shortcuts import render
from django.urls import reverse
from datetime import date, timedelta

from .models import User, Scholarship


class NewScholarshipForm(forms.Form):
    scholarship = forms.CharField(label="Scholarship Name")
    url = forms.URLField(label="Url")
    amount = forms.IntegerField(label="Amount",required=False) 
    fullride = forms.BooleanField(label="Full Ride", required=False) 
    date = forms.DateField(label="Deadline:")
    requirements = forms.CharField(label="Requirements", required=False) 
    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "scholarship/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "scholarship/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "scholarship/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "scholarship/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "scholarship/register.html")
    
@login_required
def index(request):
    return render(request, "scholarship/index.html")

@login_required
def compose(request):
    if request.method == "GET":
        return render(request, "scholarship/add.html", {
            "form": NewScholarshipForm()
        })
    elif request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    else:
        form = NewScholarshipForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            amount = "Full Ride" if data["fullride"] else str(data["amount"])
            scholarship = data["scholarship"]
            url = data["url"]
            date = data["date"]
            requirements = data["requirements"]
            scholarship = Scholarship.objects.create(scholarship=scholarship, url=url,requirements=requirements, amount= amount, date=date, category='None', user = request.user)
            scholarship.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "scholarship/add.html", {
        "form": form
    })
@login_required
def scholarships(request):
    scholarships = Scholarship.objects.filter(user=request.user).all()
    return JsonResponse([scholar.serialize() for scholar in scholarships], safe=False)
@login_required
def edit(request, scholarship_id):
    try:
        scholarship = Scholarship.objects.get(pk=scholarship_id)
    except Scholarship.DoesNotExist:
        return JsonResponse({"error": "Scholarship not found."}, status=404)
    if request.method == "GET":
        return render(request, "scholarship/edit.html", {
            "scholarship": scholarship,

        })
    elif request.method == "PUT":
        data = json.loads(request.body)
        scholarship.scholarship = data["name"]
        scholarship.url = data["url"]
        scholarship.amount = data["amount"]
        scholarship.date = data["date"]
        scholarship.requirements = data["requirements"]

        scholarship.save()
        return JsonResponse({"scholarship": scholarship.serialize()}, status=200)
@login_required
def scholarship(request, scholarship_id):
    try:
        scholarship = Scholarship.objects.get(pk=scholarship_id)
    except Scholarship.DoesNotExist:
        return JsonResponse({"error": "Scholarship not found."}, status=404)

    if request.method == "GET":
        return render(request, "scholarship/scholarship.html", {
            "scholarship": scholarship,
            "outdated": scholarship.date < date.today()
        })
        
    
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data["category"]:
            scholarship.category = data["category"]
            scholarship.save()

        scholarship.save()
        return JsonResponse({"scholarship": scholarship.serialize()}, status=200)
@login_required       
def completedview(request):
    cmpltedSchs = Scholarship.objects.filter(category="Completed").all()
    return render(request, "scholarship/completed.html", {
            "scholarships": cmpltedSchs
        })
@login_required
def recievedScholarship(request, scholarship_id):
    try:
        scholarship = Scholarship.objects.get(pk=scholarship_id)
    except Scholarship.DoesNotExist:
        return JsonResponse({"error": "Scholarship not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if "recieved" in data:
            scholarship.recieved = data["recieved"]
            scholarship.save()


        return JsonResponse({"success": "sucessfully changed recieved status"}, status=200)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)
@login_required   
def remove(request, scholarship_id):
    try:
        scholarship = Scholarship.objects.get(pk=scholarship_id)
    except Scholarship.DoesNotExist:
        return JsonResponse({"error": "Scholarship not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if "delete" in data:
            scholarship.delete()
            return JsonResponse({"success": "sucessfully deleted scholarship"}, status=200)
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


def adddocumentlink(request, scholarship_id):
    scholarship = Scholarship.objects.get(pk=scholarship_id)
    if request.method == "POST":
        link = request.POST.get("link")
        scholarship.documents.append(link)
        scholarship.save()
        return HttpResponseRedirect(reverse("scholarship", args=(scholarship_id,)))
    elif request.method == "PUT":
        data = json.loads(request.body)
        if "delete" in data:
            scholarship.documents.remove(data["link"])
            scholarship.save()  
            return JsonResponse({"message": "Link removed."})
        


