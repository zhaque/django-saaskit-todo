from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from todo.models import Item, List
import datetime
from muaccounts  import models as muamodels


class AddListForm(ModelForm):
    # slug = models.SlugField(widget=HiddenInput)
    # slug = forms.CharField(widget=forms.HiddenInput)

    # The picklist showing allowable groups to which a new list can be added
    # determines which groups the user belongs to. This queries the form object
    # to derive that list.
    def __init__(self, user, *args, **kwargs):
        super(AddListForm, self).__init__(*args, **kwargs)
        #self.fields['group'].queryset = Group.objects.filter(user=user)

    class Meta:
        model = List
        exclude = ('account')



class AddItemForm(ModelForm):
    due_date = forms.DateField(
                    required=False,
                    widget=forms.DateTimeInput(attrs={'class':'due_date_picker'})
                    )

    title = forms.CharField(
                    widget=forms.widgets.TextInput(attrs={'size':35})
                    )

    # The picklist showing the users to which a new task can be assigned
    # must find other members of the groups the current list belongs to.
    def __init__(self, task_list, muaccount, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        # print dir(self.fields['list'])
        # print self.fields['list'].initial

        membs = muaccount.members.all()
        own = User.objects.filter(id=muaccount.owner.id) # i need to do this in order to combine both
        membs = membs | own

        self.fields['assigned_to'].queryset = membs

    class Meta:
        model = Item



class EditItemForm(ModelForm):

    def __init__(self, muaccount, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)

        membs = muaccount.members.all()
        own = User.objects.filter(id=muaccount.owner.id) # i need to do this in order to combine both
        membs = membs | own

        self.fields['assigned_to'].queryset = membs



    class Meta:
        model = Item

        exclude = ('list','created_by')
