from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    
    (r'^(?P<list_slug>mine)$', 'todo.views.view_list'),
    (r'^\d{1,4}/(?P<list_slug>[\w-]+)/delete$', 'todo.views.del_list'),
    (r'^task/(?P<task_id>\d{1,6})$', 'todo.views.edit_task'),
    (r'^\d{1,4}/(?P<list_slug>[\w-]+)$', 'todo.views.view_list'),
    (r'^$', 'todo.views.list_lists'),


)

