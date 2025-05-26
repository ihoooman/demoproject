from django import forms
from .models import ChecklistQuestion


class ChecklistQuestionForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['question_text', 'order', 'active']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-field'}),
            'order': forms.NumberInput(attrs={'class': 'form-field'}),
        }