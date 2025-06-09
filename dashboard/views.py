import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, DetailView, UpdateView, FormView
from .models import Group, Subcategory, Category, Response, ChecklistQuestion
from django.contrib import messages
from .forms import * # Add CategoryForm here
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ImageUploadForm
from django.db.models import Q


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'dashboard/group_list.html'
    context_object_name = 'groups'
    login_url = 'accounts:login'

    def get_queryset(self):
        parent_id = self.kwargs.get('parent_pk')
        if parent_id:
            return Group.objects.filter(parent_id=parent_id)
        return Group.objects.filter(parent__isnull=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['parent_pk'] = self.kwargs.get('parent_pk')
        return ctx


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = Group
    fields = ['title']
    template_name = 'dashboard/group_form.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        parent_id = self.kwargs.get('parent_pk')
        if parent_id:
            form.instance.parent_id = parent_id
        return super().form_valid(form)

    def get_success_url(self):
        parent_pk = self.kwargs.get('parent_pk')
        if parent_pk:
            return reverse_lazy('dashboard:group_children', kwargs={'parent_pk': parent_pk})
        return reverse_lazy('dashboard:group_list')


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'
    login_url = 'accounts:login'


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'dashboard/subcategory_list.html'
    context_object_name = 'subcategories'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Subcategory.objects.filter(category_id=category_id)


class SubgroupFormView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'dashboard/subgroup_form.html'
    context_object_name = 'group'
    login_url = 'accounts:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()

        # Get questions that are:
        # 1. Global (no group specified)
        # 2. For this subgroup's parent group (with no specific subgroup)
        # 3. Specifically for this subgroup
        context['questions'] = ChecklistQuestion.objects.filter(
            Q(active=True) & (
                    Q(group__isnull=True) |  # Global questions
                    Q(group=group.parent, subgroup__isnull=True) |  # Questions for parent with no specific subgroup
                    Q(subgroup=group)  # Questions specifically for this subgroup
            )
        ).order_by('order')

        return context
class ChecklistSettingsView(LoginRequiredMixin, ListView):
    model = ChecklistQuestion
    template_name = 'dashboard/checklist_settings.html'
    context_object_name = 'questions'
    login_url = 'accounts:login'


class ChecklistQuestionCreateView(LoginRequiredMixin, CreateView):
    model = ChecklistQuestion
    form_class = ChecklistQuestionForm
    template_name = 'dashboard/checklist_question_form.html'
    success_url = reverse_lazy('dashboard:checklist_settings')
    login_url = 'accounts:login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class ChecklistQuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = ChecklistQuestion
    form_class = ChecklistQuestionForm
    template_name = 'dashboard/checklist_question_form.html'
    success_url = reverse_lazy('dashboard:checklist_settings')
    login_url = 'accounts:login'


@login_required
@require_POST
def delete_group(request, pk):
    try:
        group = Group.objects.get(pk=pk)
        group.delete()
        return JsonResponse({'status': 'success'})
    except Group.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Group not found'}, status=404)


@login_required
@require_POST
def delete_multiple_groups(request):
    data = json.loads(request.body)
    group_ids = data.get('group_ids', [])

    try:
        Group.objects.filter(pk__in=group_ids).delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def save_responses(request, category_id):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('q_') and value.strip():
                # Format: q_questionNumber_subcategoryId
                parts = key.split('_')
                if len(parts) == 3:
                    question_num = parts[1]
                    subcategory_id = parts[2]

                    subcategory = Subcategory.objects.get(id=subcategory_id)
                    question_text = f"Question {question_num}"

                    Response.objects.create(
                        subcategory=subcategory,
                        user=request.user,
                        question=question_text,
                        answer=value
                    )

        return redirect('dashboard:subcategories', pk=category_id)
    return redirect('dashboard:categories')


@login_required
def save_subgroup_responses(request, group_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=group_id)

        # Save responses for each question
        for key, value in request.POST.items():
            if key.startswith('question_') and value.strip():
                # Format: question_id
                question_id = key.split('_')[1]
                question = get_object_or_404(ChecklistQuestion, pk=question_id)

                Response.objects.create(
                    user=request.user,
                    group=group,
                    question=question.question_text,
                    answer=value
                )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'}, status=400)


@login_required
@require_POST
def delete_checklist_question(request, pk):
    try:
        question = ChecklistQuestion.objects.get(pk=pk)
        question.delete()
        return JsonResponse({'status': 'success'})
    except ChecklistQuestion.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Question not found'}, status=404)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title']
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:categories')
    login_url = 'accounts:login'


def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('dashboard:categories')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'dashboard/category_form.html', {
        'form': form,
        'category': category,
        'is_edit': True
    })


def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('dashboard:categories')


class SubcategoryListView(LoginRequiredMixin, ListView):
    model = Subcategory
    template_name = 'dashboard/subcategory_list.html'
    context_object_name = 'subcategories'
    login_url = 'accounts:login'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Subcategory.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return context


class SubcategoryCreateView(LoginRequiredMixin, CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'dashboard/subcategory_form.html'
    login_url = 'accounts:login'

    def form_valid(self, form):
        category_id = self.kwargs.get('pk')
        form.instance.category_id = category_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard:subcategories', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context['is_edit'] = False
        return context


class SubcategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'dashboard/subcategory_form.html'
    login_url = 'accounts:login'

    def get_success_url(self):
        return reverse_lazy('dashboard:subcategories', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category
        context['is_edit'] = True
        return context


@login_required
def subcategory_delete(request, pk):
    subcategory = get_object_or_404(Subcategory, pk=pk)
    category_id = subcategory.category.pk
    subcategory.delete()
    messages.success(request, 'Subcategory deleted successfully!')
    return redirect('dashboard:subcategories', pk=category_id)


class UploadCenterView(View):
    def get(self, request):
        images = UploadedImage.objects.all().order_by('-uploaded_at')
        form = ImageUploadForm()
        return render(request, 'dashboard/upload_center.html', {'images': images, 'form': form})

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            if request.user.is_authenticated:
                image.user = request.user
            image.save()
            messages.success(request, 'Image uploaded successfully!')
            return redirect('dashboard:upload_center')
    return redirect('dashboard:upload_center')

def delete_image(request, pk):
    image = get_object_or_404(UploadedImage, pk=pk)
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Image deleted successfully!')
    return redirect('dashboard:upload_center')