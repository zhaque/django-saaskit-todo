from django.db import models
from django.forms.models import ModelForm
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from muaccounts  import models as muamodels

import string, datetime

class ListManager(models.Manager):
    """
    Retrieves all incomplete tasks for a given list.
    """
    def get_query_set(self):
        return super(ListManager, self).get_query_set().filter(completed=0)

class List(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60,editable=False)

    #group = models.ForeignKey(Group)
    account = models.ForeignKey(muamodels.MUAccount)

    def save(self):
        if not self.id:
            # Replace spaces in slug with hyphens, and lowercase.
            self.slug = (self.name).lower().replace(' ','-')

            # Regex to remove non-alphanumeric chars, using re (regular experession module)
            # If we end up with double hyphens, remove those too.
            import re
            self.slug = re.sub(r"[^A-Za-z0-9\-]", "", self.slug).replace('--','-')

            super(List, self).save()

    def __unicode__(self):
        return self.name

    # Custom manager lets us do things like Item.completed_tasks.all()
    objects = models.Manager()
    incomplete_tasks = ListManager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Lists"

        # Prevents (at the database level) creation of two lists with the same name in the same group
        unique_together = ("account", "slug")





class Item(models.Model):
    title = models.CharField(max_length=140)
    list = models.ForeignKey(List)
    created_date = models.DateField()
    due_date = models.DateField(blank=True,null=True,)
    completed = models.BooleanField()
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    assigned_to = models.ForeignKey(User, related_name='todo_assigned_to')
    note = models.TextField(blank=True)
    priority = models.PositiveIntegerField(max_length=3)

    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title

    # Auto-set the item creation / completed date
    def save(self):
        # Set datetime on initial item save
        if not self.id:
            self.created_date = datetime.datetime.now()

        # If Item is being marked complete, set the completed_date
        if self.completed :
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]


class Comment(models.Model):
    """
    Not using Django's built-in comments becase we want to be able to save
    a comment and change task details at the same time. Rolling our own since it's easy.
    """
    author = models.ForeignKey(User)
    task = models.ForeignKey(Item)
    date = models.DateTimeField(default=datetime.datetime.now)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return '%s - %s' % (
                self.author,
                self.date,
                )