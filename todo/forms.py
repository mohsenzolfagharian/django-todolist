from django.forms import ModelForm
from .models import TODO


class TodoForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'memo', 'important']



