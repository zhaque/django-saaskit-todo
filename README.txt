--------------------
ABOUT DJANGO-TODO
--------------------

Version 0.9.3

Scot Hacker - shacker at birdhouse dot org

django-todo is a pluggable multi-user, multi-group task management and assignment application for Django. 

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
JQuery with UI/DatePicker. The sample templates provided include a JQuery date picker.

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

list_lists.html
view_list.html
del_list.html
edit_task.html

Sample templates and media (CSS, images) are included in the "samples" folder, but are NOT supported. 
To use them, copy them from the "samples" dir to corresponding locations in your project dir,
making sure your SITE_MEDIA URL is wired up correctly. Feel free to modify these or create your own. 

--------------------
INSTALLATION
--------------------

0) Recommended: Install django-registration (or build your own auth system) and make sure you can 
log in at /accounts/login .  In Admin, make sure you've created at least one group and one user 
belonging to that group.

1) Put django-todo/tasks somewhere on your Python path.

2) In settings.py:


    INSTALLED_APPS = (
        ...
        'todo',
    )    

    # This assumes you're serving static media from /site_media
    TODO_MEDIA_URL = '/site_media/todo/' 

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "todo.context_processors.todo_vars",
    )


3) To set up your database, run:

	python manage.py syncdb

4) Add to your URL conf:

	(r'^todo/', include('todo.urls')),


5) Add a "todo" symlink from your project's media directory to the application's media directory, e.g.

    cd ~/mysites/myproject/media
    ln -s /path/to/app/dir/django-todo/todo/media/todo todo


6) Log in as that user and access /todo


--------------------
Versions
--------------------

0.9.5 - Fixed jquery bug when editing existing events - datepicker now shows correct date.
        Removed that damned Django pony from base template.

0.9.4 - Replaced str with unicode in models. Fixed links back to lists in "My Tasks" view.

0.9.3 - Missing link to the individual task editing view

0.9.2 
    - Now fails gracefully when trying to add a 2nd list with the same name to the same group. 
    - Due dates for tasks are now truly optional.
    - Corrected datetime editing conflict when editing tasks
    - Max length of a task name has been raised from 60 to 140 chars. 
        If upgrading, please modify your database accordingly (field todo_item.name = maxlength 140).
    - Security: Users supplied with direct task URLs can no longer view/edit tasks outside their group scope
        Same for list views - authorized views only.
    - Correct item and group counts on homepage (note - admin users see ALL groups, not just the groups they "belong" to)

0.9.1 - Removed context_processors.py - leftover turdlet

0.9 - First release

--------------------
TODO ITEMS for django-todo
--------------------

- Send email to task assignees before a task is due

- Provide RSS feeds of assigned tasks, list tasks, and group tasks.

- URL of a list view should reference the group name, not group ID. But groups don't have slugs by default, so would have to extend the Group model...


--------------------
THANKS 

To @mandric for all the assistance!
--------------------
