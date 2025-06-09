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
        fields = ['question_text', 'group', 'subgroup', 'active_system', 'active', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(
            queryset=Group.objects.filter(parent__isnull=True),
            required=False,
            label="Apply to Group",
            widget=forms.Select(attrs={'class': 'form-field'})
        )
        self.fields['subgroup'] = forms.ModelChoiceField(
            queryset=Group.objects.filter(parent__isnull=False),
            required=False,
            label="Apply to Subgroup",
            widget=forms.Select(attrs={'class': 'form-field'})
        )
        self.fields['active_system'] = forms.ChoiceField(
            choices=ChecklistQuestion.SYSTEM_CHOICES,
            required=True,
            label="System Active",
            widget=forms.RadioSelect()
        )

    def clean(self):
        cleaned_data = super().clean()
        group = cleaned_data.get('group')
        subgroup = cleaned_data.get('subgroup')

        # If subgroup is selected but no group, set the group to the parent
        if subgroup and not group:
            cleaned_data['group'] = subgroup.parent

        # If neither group nor subgroup are selected, raise validation error
        if not group and not subgroup:
            raise forms.ValidationError("You must select either a group or a subgroup")

        return cleaned_data
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['title', 'image']