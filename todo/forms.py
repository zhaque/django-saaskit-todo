from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from todo.models import Item, List

class AddListForm(ModelForm):
    # slug = models.SlugField(widget=HiddenInput)
    # slug = forms.CharField(widget=forms.HiddenInput) 
    
    # The picklist showing allowable groups to which a new list can be added
    # determines which groups the user belongs to. This queries the form object
    # to derive that list.
    def __init__(self, user, *args, **kwargs):
        super(AddListForm, self).__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)

    class Meta:
        model = List
        

        
class AddItemForm(ModelForm):
    due_date = forms.DateField(
                    required=False,
                    widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                    )
                    
    name = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':45})
                    ) 

    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current user belongs to.
    def __init__(self, user, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(groups__in=user.groups.all()).distinct()
        
    class Meta:
        model = Item
        


class EditItemForm(ModelForm):
    

    class Meta:
        model = Item        