from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    context = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}))

    class Meta:
        model = Message
        fields = ['context']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['context'].label = ''