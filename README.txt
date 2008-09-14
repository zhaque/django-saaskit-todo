--------------------
ABOUT DJANGO-TODO
--------------------

Version 0.9
Scot Hacker - shacker at birdhouse dot org

django-todo is a multi-user, multi-group task management and assignment system. 

The assumption is that your organization/publication/company has multiple groups of employees,
each with multiple users. Users may belong to multiple groups, and each group can have multiple todo lists.

Users can view and modify all to-do lists belonging to their group(s). 
Only users with is_staff() can delete lists. 

You must have at least one Group set up in Django admin, and that group must have at least one User as a member.
This is true even if you're the sole user of django-todo. 

Identical list names can exist in different groups, but not in the same group.

django-todo provides the following URLs/views:

/todo - View a list of lists belonging to groups the current user is a member of, and create new lists in those groups
/todo/[group_id]/[slug] - View a specific list, or add tasks to list. Mark task items as complete/incomplete
/todo/[group_id]/[slug]/delete - Delete a list (is_staff() users only)
/todo/mine - Show tasks assigned specifically to the currently logged in user, irrespective of list
/todo/[slug]/task/[ID] - Edit an existing task (change name, reassign, change due date)

--------------------
REQUIREMENTS
--------------------

All views are login-required. Unauthenticated users will be redirected to the default /accounts/login.
All tasks are "created by" the current user and "assigned to" a specific user (default is same user).
Therefore, you must have a user authentication system (login/logout system) working first. 
You can build it yourself per http://docs.djangoproject.com/en/dev/topics/auth/ , or use 
django-registration (though you may want to disable open registration if you do that).

Task due dates can be entered manually, but for ease of use, try a JavaScript date picker. I recommend
JQuery with UI/DatePicker. The sample templates provided with django-todo assume its presence.

http://jquery.com/
http://docs.jquery.com/UI/Datepicker

To get the datepicker working, use something like this, either in base.html or in this app's templates:

<script type="text/javascript" src="/site_media/js/jquery-1.2.6.min.js"></script>
<script type="text/javascript" src="/site_media/js/ui.datepicker.js"></script>    

<script type="text/javascript" charset="utf-8">
    $(document).ready(function(){
        $('#id_due_date').datepicker();
     });
</script>

--------------------
TEMPLATES AND MEDIA
--------------------

django-todo requires the following templates to be living in templates/todo:

todo/list_lists.html
todo/view_list.html
todo/del_list.html
todo/edit_task.html

Sample templates and media (CSS, images) are included in the "samples" folder, but are NOT supported. 
To use them, copy them from the "samples" dir to corresponding locations in your project dir,
making sure your SITE_MEDIA URL is wired up correctly. Feel free to modify these or create your own. 

--------------------
INSTALLATION
--------------------

0) Recommended: Install django-registration (or build your own auth system) and make sure you can log in at /accounts/login

1) Put django-todo/tasks somewhere on your Python path.

2) Add 'todo' to your INSTALLED_APPS

3) To set up your database, run:

	python manage.py syncdb

3) Add to your URL conf:

	(r'^todo/', include('todo.urls')),

4) In Admin, make sure you've created at least one group and one user belonging to that group.

5) Log in as that user and access /todo


--------------------
Versions
--------------------

1.0 - First release

--------------------
TODO ITEMS for django-todo
--------------------

- Send email to task assignees before a task is due

- Provide RSS feeds of assigned tasks, list tasks, and group tasks.

- URL of a list view should reference the group name, not group ID. But groups don't have slugs by default, so would have to extend the Group model...

- Due Dates really should be optional (they already should be - not sure why it's behaving as if required)

- Total item count is for all items, not just items in the user's groups

- Fails correctly when trying to add a new list if the same list name already exists in the same group, but doesn't fail elegantly.

- Tagging (probably best served by django-tagging)
