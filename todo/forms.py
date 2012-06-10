from django import forms
from todo.models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('name',)


class TodoListForm(forms.Form):
    def __init__(self, *args, **kwargs):
        todos = kwargs.pop('todos', [])
        super(TodoListForm, self).__init__(*args, **kwargs)
        self.done_items = []
        for todo in todos:
            field = str(todo.id)
            if todo.is_done:
                self.done_items.append(field)
            self.fields[field] = forms.BooleanField(
                required=False, label=todo.name)

    def clean(self):
        selected = [tid for tid, val in self.cleaned_data.items() if val]
        if not selected:
            raise forms.ValidationError("You need to select one or more items.")
        return selected
