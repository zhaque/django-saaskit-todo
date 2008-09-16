from django.conf import settings

def todo_vars(request):
    return {'TODO_MEDIA_URL': settings.TODO_MEDIA_URL}
