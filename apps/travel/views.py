# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
import bcrypt
from .models import Users, Trips

# Create your views here.
def index(request):
    if 'errors' not in request.session:
        request.session['errors'] = []
    context = {
        "errors": request.session['errors']
    }
    return render(request, 'travel/index.html', context)

def register(request):
    request.session['errors'] = Users.objects.validator(request.POST)
    if 'username' not in request.session:
        request.session['username'] = request.POST['username']
    else:
        request.session['username'] = request.POST['username']
    if request.session['errors']['name'] == "" and request.session['errors']['username'] == "" and request.session['errors']['pw'] == "" and request.session['errors']['cpw'] == "": 
        Users.objects.create(name=request.POST['name'],username=request.POST['username'],password=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()))
        user_id = Users.objects.get(username=request.POST['username']).id 
        request.session['id'] = user_id 
        return redirect('/success')
    else: 
        return redirect('/')

def login(request):
    request.session['errors'] = Users.objects.logincheck(request.POST)   
    if request.session['errors']['login'] == "":
        user_id = Users.objects.get(username=request.POST['username']).id 
        request.session['id'] = user_id 
        return redirect('/success')
    else: 
        return redirect('/')

def success(request):
    user_id = request.session['id']
    context = {
        "name": Users.objects.get(id=user_id).username,
        "trips": Trips.objects.filter(owner__id=user_id),
        "joined": Trips.objects.filter(attendees__id=user_id),
        "others": Trips.objects.exclude(owner__id=user_id),
    }
    return render(request, 'travel/dashboard.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def addtrip(request):
    context = {
        "errors": request.session['errors']
    }
    return render(request, 'travel/addtrip.html',context)

def newtrip(request):
    owner = Users.objects.get(id=request.session['id'])
    request.session['errors'] = Trips.objects.tripcheck(request.POST)
    if request.session['errors']['addtrip'] == "":
        Trips.objects.create(owner=owner,destination=request.POST['destination'],description=request.POST['description'],start=request.POST['start'],end=request.POST['end'])
        return redirect('/success')
    else: 
        return redirect('/addtrip')

def destination(request,id):
    context = {
        "trip":Trips.objects.get(id=id),
        "attendees":Trips.objects.get(id=id).attendees.all()
    }
    return render(request, 'travel/destination.html',context)

def join(request,id):
    user = Users.objects.get(id=request.session['id'])
    Trips.objects.get(id=id).attendees.add(user)
    return redirect('/success')