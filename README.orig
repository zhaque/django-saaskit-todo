--------------------
ABOUT DJANGO-TODO
--------------------
 
Version 1.1

Scot Hacker - shacker at birdhouse dot org

django-todo is a pluggable multi-user, multi-group task management and assignment application for Django. 
In many organizations, django-todo can serve as a complete, working ticketing system.

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
/todo/[slug]/task/[ID] - View/edit an existing task (change name, reassign, change due date)

--------------------
REQUIREMENTS
--------------------

Take care of these items before installing django-todo:


1) An existing Django project site, with media and templates dirs wired up and working. 
    

2) To take advantage of the ajaxy stuff, you'll need a reference to the main jquery 
library and jquery-ui (http://jqueryui.com/download) in your templates. 
django-todo supplies an additional jquery module in its own media subdirectory but 
assumes that jquery and jquery-ui are already present. Your project templates should 
include something like this in the head:

<link type="text/css" href="/media/js/jquery-ui-1.7.1.custom.css" rel="Stylesheet" />
<script type="text/javascript" src="/media/js/jquery-1.3.2.min.js"></script>
<script type="text/javascript" src="/media/js/ui.core.js"></script>

Tweak as necessary. 

django-todo pages that require it will insert additional CSS/JavaScript into page heads,
so your project's base templates must include:

{% block extrahead %}{% endblock %}



3) All views in django-todo are for registered users only, so you'll need a full login
system. I suggest setting up django-registration if you don't have it already.

4) Make sure your project is set up to send smtp email, i.e. you have something like this in your settings:

EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.domain.com'
EMAIL_HOST_USER = 'sysmail@domain.com'
DEFAULT_FROM_EMAIL = 'sysmail@domain.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587


5) All views are login-required. Unauthenticated users will be redirected to the default /accounts/login.
All tasks are "created by" the current user and "assigned to" a specific user (default is same user).
Therefore, you must have a user authentication system (login/logout system) working first. 
You can build it yourself per http://docs.djangoproject.com/en/dev/topics/auth/ , or use 
django-registration (though you may want to disable open registration if you do that).

Task due dates can be entered manually, but for ease of use, try a JavaScript date picker. I recommend
JQuery with UI/DatePicker. 




--------------------
INSTALLATION
--------------------


1) Put django-todo/todo somewhere on your Python path.

2) In settings.py:


    INSTALLED_APPS = (
        ...
        'todo',
    )    


3) To set up your database, run:

	python manage.py syncdb


4) Add to your URL conf:

	(r'^todo/', include('todo.urls')),



5) Connect up the distributed media and templates to your project

    Either copy django-todo's media/todo and templates/todo dirs into your 
    project's "media" and "templates" dirs, or create symlinks: 

    cd /path/to/myproject/media
    ln -s /path/to/django-todo/todo/media/todo todo

    cd /path/to/myproject/templates
    ln -s /path/to/django-todo/todo/templates/todo todo



6) Add two links to your site's navigation system:
        <a href="{% url todo-lists %}">To-do Lists</a>
        <a href="{% url todo-mine %}">My Tasks</a>


7) Log in and access /todo


--------------------
Versions
--------------------

1.1 -   Completion date was set properly when checking items off a list, but not when saving from an Item
        detail page. Added a save method on Item to fix. Fixed documentation bug re: context_processors. 
        Newly added comments are now emailed to everyone who has participated in a thread on a task.

1.0.1 - When viewing a single task that you want to close, it's useful to be able to comment on and 
        close a task at the same time. We were using django-comments so these were different models
        in different views. Solution was to stop using django-comments and roll our own, then rewire
        the view. Apologies if you were using a previous version - you may need to port over your comments
        to the new system.

1.0.0 - Major upgrade to release version. Drag and drop task prioritization. E-mail notifications
        (now works more like a ticket system). More attractive date picker. Bug fixes.

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

- Provide RSS feeds of assigned tasks, list tasks, and group tasks.


--------------------
THANKS 

To @mandric for all the assistance!

