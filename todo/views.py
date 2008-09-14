from django import forms 
from django.shortcuts import render_to_response
from todo.models import Item, List
from todo.forms import AddListForm, AddItemForm, EditItemForm
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.template import RequestContext
import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required
def list_lists(request):

    """
    Homepage view - list of lists a user can view, and ability to add a list.
    """
    
    # Make sure belongs to at least one group.
    group_count = request.user.groups.all().count()
    if group_count == 0:
        request.user.message_set.create(message="You do not yet belong to any groups. Ask your administrator to add you to one.")
        

    # Only show lists to the user that belong to groups they are members of.
    # Staff users see all lists
    if request.user.is_staff:
        list_list = List.objects.all().order_by('name')
    else:
        list_list = List.objects.filter(group__in=request.user.groups.all).order_by('name')
    
    # Count everything
    list_count = list_list.count()
    item_count = Item.objects.count()
    
    
    if request.POST:    
        form = AddListForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="A new list has been added.")
            return HttpResponseRedirect(request.path)
            
    else:
        form = AddListForm(request.user)
            
    
    return render_to_response('todo/list_lists.html', locals(), context_instance=RequestContext(request))  
    

@login_required
def del_list(request,list_slug):

    """
    Delete an entire list. Danger Will Robinson! Only staff members should be allowed to access this view.
    """
    
    if request.user.is_staff:
        can_del = 1

    # Get this list's object (to derive list.name, list.id, etc.)
    list = get_object_or_404(List, slug=list_slug)

    # If delete confirmation is in the POST, delete all items in the list, then kill the list itself
    if request.method == 'POST':
        # Can the items
        del_items = Item.objects.filter(list=list.id)
        for del_item in del_items:
            del_item.delete()
        
        # Kill the list
        del_list = List.objects.get(id=list.id)
        del_list.delete()
        
        # A var to send to the template so we can show the right thing
        list_killed = 1

    else:
        item_count_done = Item.objects.filter(list=list.id,completed=1).count()
        item_count_undone = Item.objects.filter(list=list.id,completed=0).count()
        item_count_total = Item.objects.filter(list=list.id).count()    
    
    return render_to_response('todo/del_list.html', locals(), context_instance=RequestContext(request))


@login_required
def view_list(request,list_slug):
    
    """
    Display and manage items in a task list
    """
    
    # First check for items in the mark_done POST array. If present, change
    # their status to complete.
    if request.POST.getlist('mark_done'):
        done_items = request.POST.getlist('mark_done')
        # Iterate through array of done items and update its representation in the model
        for thisitem in done_items:
        	p = Item.objects.get(id=thisitem)
        	p.completed = 1
        	p.completed_date = datetime.datetime.now()
        	p.save()
	        request.user.message_set.create(message="Item marked complete.")
	        
	
	# Undo: Set completed items back to incomplete
    if request.POST.getlist('undo_completed_task'):
        undone_items = request.POST.getlist('undo_completed_task')
        for thisitem in undone_items:
        	p = Item.objects.get(id=thisitem)
        	p.completed = 0
        	p.save()
	        request.user.message_set.create(message="Previously completed task marked incomplete.")	        
        	

    # And delete any requested items
    if request.POST.getlist('del_task'):
        deleted_items = request.POST.getlist('del_task')
        for thisitem in deleted_items:
        	p = Item.objects.get(id=thisitem)
        	p.delete()
	        request.user.message_set.create(message="Item deleted.")
        	
    # And delete any *already completed* items
    if request.POST.getlist('del_completed_task'):
        deleted_items = request.POST.getlist('del_completed_task')
        for thisitem in deleted_items:
        	p = Item.objects.get(id=thisitem)
        	p.delete()
	        request.user.message_set.create(message="Deleted previously completed item.")


    thedate = datetime.datetime.now()
    created_date = "%s-%s-%s" % (thedate.year, thedate.month, thedate.day)


    # Get list of items with this list ID, or filter on items assigned to me
    if list_slug == "mine":
        task_list = Item.objects.filter(assigned_to=request.user, completed=0)
        completed_list = Item.objects.filter(assigned_to=request.user, completed=1)
        # item = Item.objects.get(pk=1)
        # item.overdue_status()
        
    else:
        list = get_object_or_404(List, slug=list_slug)
        listid = list.id
        task_list = Item.objects.filter(list=list.id, completed=0)
        completed_list = Item.objects.filter(list=list.id, completed=1)

    
    if request.POST.getlist('add_task'):
        form = AddItemForm(request.user, request.POST,initial={
        'assigned_to':request.user.id,
        
        })
        
        if form.is_valid():
            form.save()
            # confirmation = "A new task has been added." 
            request.user.message_set.create(message="A new task has been added.")
            return HttpResponseRedirect(request.path)

    else:
        form = AddItemForm(request.user, initial={
            'assigned_to':request.user.id,
            } )


    if request.user.is_staff:
        can_del = 1

    return render_to_response('todo/view_list.html', locals(), context_instance=RequestContext(request))
    


@login_required
def edit_task(request,task_id):

    """
    Allow task details to be edited.
    """
    
    task = get_object_or_404(Item, pk=task_id)

    if request.POST:    
         form = EditItemForm(request.POST,instance=task)
         if form.is_valid():
             form.save()
             request.user.message_set.create(message="The task has been edited.")
             return HttpResponseRedirect('/todo/%s/%s' % (task.list.id, task.list.slug))
             

    else:
        form = EditItemForm(instance=task)


    return render_to_response('todo/edit_task.html', locals(), context_instance=RequestContext(request))