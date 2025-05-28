from django import forms
from .models import Category, Subcategory, ChecklistQuestion


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['title']


class ChecklistQuestionForm(forms.ModelForm):
    class Meta:
        model = ChecklistQuestion
        fields = ['question_text', 'active']