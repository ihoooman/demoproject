
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import GroupListView, GroupCreateView, delete_group, delete_multiple_groups

app_name = 'dashboard'

urlpatterns = [
    # Group management URLs
    path('', GroupListView.as_view(), name='group_list'),
    path('group/add/', GroupCreateView.as_view(), name='group_add'),
    path('group/<int:parent_pk>/children/', GroupListView.as_view(), name='group_children'),
    path('group/<int:parent_pk>/add/', GroupCreateView.as_view(), name='group_add_child'),
    path('group/<int:pk>/form/', views.SubgroupFormView.as_view(), name='subgroup_form'),
    path('group/<int:group_id>/save-responses/', views.save_subgroup_responses, name='save_subgroup_responses'),

    # Delete functionality
    path('group/<int:pk>/delete/', delete_group, name='group_delete'),
    path('groups/delete/', delete_multiple_groups, name='groups_delete'),

    # Category management URLs
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.SubcategoryListView.as_view(), name='subcategories'),
    path('categories/<int:category_id>/save/', views.save_responses, name='save_responses'),

    # Checklist settings
    path('checklist-settings/', views.ChecklistSettingsView.as_view(), name='checklist_settings'),
    path('checklist-settings/add/', views.ChecklistQuestionCreateView.as_view(), name='checklist_question_add'),
    path('checklist-settings/<int:pk>/edit/', views.ChecklistQuestionUpdateView.as_view(),
         name='checklist_question_edit'),
    path('checklist-settings/<int:pk>/delete/', views.delete_checklist_question, name='checklist_question_delete'),

    # Administrative URLs
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]