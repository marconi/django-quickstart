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
        for todo in todos:
            field = str(todo.id)
            self.fields[field] = forms.BooleanField(
                required=False, label=todo.name)
            self.fields[field].todo = todo

    def clean(self):
        data = self.cleaned_data
        selected = filter(lambda item: True if item[1] else False, data.items())
        if not selected:
            raise forms.ValidationError("You need to select one or more items.")
        return [key for key, _ in selected]
