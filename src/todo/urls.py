from django.conf.urls import patterns, url

urlpatterns = patterns('todo.views',
    url(r'^new/$', 'new_todo', name='new_todo'),
)
