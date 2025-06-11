
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import GroupListView, GroupCreateView, delete_group, delete_multiple_groups
from django.conf import settings
#from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
app_name = 'dashboard'


urlpatterns = [
    # Group management URLs
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }),

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

    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('categories/<int:category_id>/save-responses/', views.save_responses, name='save_responses'),
    path('categories/<int:category_id>/subcategory/add/', views.SubcategoryCreateView.as_view(), name='subcategory_add'),

    path('upload-center/', views.UploadCenterView.as_view(), name='upload_center'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete_image'),

    path('api/', include('dashboard.api_urls')),

]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)