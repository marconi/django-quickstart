from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from todo.forms import TodoListForm, TodoForm
from todo.models import Todo


def home(request):
    todos=Todo.objects.order_by('-created')
    if request.method == 'POST':
        action = request.POST['action'].lower()
        todo_list_form = TodoListForm(data=request.POST, todos=todos)
        if todo_list_form.is_valid():
            selected = Todo.objects.filter(id__in=todo_list_form.cleaned_data)
            actions = {'done': lambda items: items.update(is_done=True),
                       'delete': lambda items: items.delete()}
            actions.get(action)(selected)
            messages.add_message(request, messages.SUCCESS,
                                 'Items has been updated.')
        else:
            messages.add_message(request, messages.ERROR,
                                 ''.join(todo_list_form.non_field_errors()))
        return redirect('home')
    else:
        todo_form = TodoForm()
        todo_list_form = TodoListForm(todos=todos)
    context = {'todo_list_form': todo_list_form,
               'todo_form': todo_form}
    return render_to_response('todo/home.html',
                              context,
                              RequestContext(request))

def new_todo(request):
    if not request.method == 'POST':
        return redirect('home')
    todo_form = TodoForm(request.POST)
    if todo_form.is_valid():
        todo_form.save()
        messages.add_message(request, messages.SUCCESS,
                             'Item has been added.')
    else:
        messages.add_message(request, messages.ERROR,
                             'You need to enter a name.')
    return redirect('home')
