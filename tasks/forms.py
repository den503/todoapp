from django import forms
from tasks.models import TodoItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description', 'priority', )
        labels = {'description': 'Описание', 'priority': ''}


class TodoItemExportForm(forms.Form):
    priority_high = forms.BooleanField(label='высокой сложности', initial=True, required=False)
    priority_medium = forms.BooleanField(label='средней сложности', initial=True, required=False)
    priority_low = forms.BooleanField(label='низкой сложности', initial=False, required=False)
