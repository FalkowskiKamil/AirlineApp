from django import forms
from .models import Message, MessageAnswer

class MessageForm(forms.ModelForm):
    context = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), label=False)

    class Meta:
        model = Message
        fields = ['context']

class MessageAnswerForm(forms.ModelForm):
    context = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), label=False)

    class Meta:
        model = MessageAnswer
        fields = ['context']