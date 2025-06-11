# dashboard/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (GroupViewSet, CategoryViewSet, SubcategoryViewSet,
                       ChecklistQuestionViewSet, ResponseViewSet)

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'questions', ChecklistQuestionViewSet)
router.register(r'responses', ResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]