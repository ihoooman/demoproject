from django import forms
from .models import *
from accounts.models import UploadedImage  # Add this import


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
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']