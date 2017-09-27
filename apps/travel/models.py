# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re 
from datetime import date
import datetime

# Create your models here.
errors = {}
chars = r'[a-zA-Z]{3,}'
chars = re.compile(chars)

class UserManager(models.Manager):
    def validator(self,postData):
        errors['login'] = ""
        if chars.match(postData['name']):
            errors['name'] = ""
        else: 
            errors['name'] = "Name must be at least three characters and only contain letters"
        if chars.match(postData['username']):
            errors['username'] = ""
        else: 
            errors['username'] = "Username must be at least three characters and only contain letters"
        if len(Users.objects.filter(username=postData['username'])) != 0:
            errors['username'] = "Username already in use"
        if len(postData['pw']) > 7:
            errors['pw'] = ""
        else: 
            errors['pw'] = "Password must be at least 8 characters"
        if postData['cpw'] == postData['pw']:
            errors['cpw'] = ""
        else:
            errors['cpw'] = "Password Confirmation must match Password "
        return errors

    def logincheck(self,postData):
        errors['name'] = ""
        errors['username'] = ""
        errors['pw'] = ""
        errors['cpw'] = ""
        if not chars.match(postData['username']):
            errors['login'] = "Please enter a valid username (alphabet only, at least three characters)"
        elif len(Users.objects.filter(username=postData['username'])) == 0:
            errors['login'] = "Username not registered"
        elif not bcrypt.checkpw(postData['pw'].encode(), Users.objects.filter(username=postData['username'])[0].password.encode()):
            errors['login'] = "Password incorrect"
        else:
            errors['login'] = ""
        return errors
        
class TripManager(models.Manager):
    def tripcheck(self,postData):
        # These were a bunch of tests I tried to compare dates. I could compare the two dates but not the start date to today. 
        # print postData['start']
        # print date.today()
        # start_date = datetime.datetime.strptime(postData['start'], '%Y-%m-%dT')
        # print start_date
        # if postData['start'] < postData['end']:
        #     print "nope"
        # elif postData['start'] > postData['end']:
        #     print "not unless you time travel "
        if len(postData['destination']) < 1 or len(postData['description']) < 1:
            errors['addtrip'] = "Destination and Description cannot be left empty"
        elif postData['start'] > postData['end']:
            errors['addtrip'] = "End Date cannot come before Start Date"
        else:
            errors['addtrip'] = ""
        return errors 

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Trips(models.Model):
    owner = models.ForeignKey(Users,related_name='mytrips')
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    attendees = models.ManyToManyField('Users',related_name='jointrips')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripManager()