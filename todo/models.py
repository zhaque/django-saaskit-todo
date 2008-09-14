from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
import string, datetime


class List(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60,editable=False)
    group = models.ForeignKey(Group)
    
    def save(self):
        if not self.id:
            # Replace spaces in slug with hyphens, and lowercase.
            self.slug = (self.name).lower().replace(' ','-')
            
            # Regex to remove non-alphanumeric chars, using re (regular experession module)
            # If we end up with double hyphens, remove those too.
            import re
            self.slug = re.sub(r"[^A-Za-z0-9\-]", "", self.slug).replace('--','-')
            
        super(List, self).save()

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ["name"]        
        verbose_name_plural = "Lists"
        
        # We shouldn't have two lists with the same name in the same group
        unique_together = ("group", "slug")
        
        
        
class Item(models.Model):
    name = models.CharField(max_length=60)
    list = models.ForeignKey(List)
    created_date = models.DateField()    
    due_date = models.DateField(blank=True,null=True,)
    completed = models.BooleanField()
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    assigned_to = models.ForeignKey(User, related_name='assigned_to')
    
    PRIORITY_CHOICES = (
         ('1', '1'),
         ('2', '2'),
         ('3', '3'),
         ('4', '4'),
         ('5', '5'),                                    
     )
    priority = models.PositiveIntegerField(max_length=1, choices=PRIORITY_CHOICES,default=3)
    
    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __str__(self):
        return self.name
        
    # Auto-set the item creation date
    def save(self):
        # Set datetime on initial item save (better than deprecated auto_now_add)
        if not self.id:
            self.created_date = datetime.datetime.now()
            # print self.created_date
        else:
            # print self.created_date
            pass
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]        
        
