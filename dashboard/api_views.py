# dashboard/api_views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response as DRFResponse
from django.shortcuts import get_object_or_404
from .models import Group, Category, Subcategory, ChecklistQuestion, Response
from .serializers import (GroupSerializer, CategorySerializer, SubcategorySerializer,
                          ChecklistQuestionSerializer, ResponseSerializer)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, methods=['get'])
    def children(self, request, pk=None):
        children = Group.objects.filter(parent=pk)
        serializer = self.get_serializer(children, many=True)
        return DRFResponse(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        subcategories = Subcategory.objects.filter(category_id=pk)
        serializer = SubcategorySerializer(subcategories, many=True)
        return DRFResponse(serializer.data)


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class ChecklistQuestionViewSet(viewsets.ModelViewSet):
    queryset = ChecklistQuestion.objects.all()
    serializer_class = ChecklistQuestionSerializer

    def get_queryset(self):
        queryset = ChecklistQuestion.objects.all()
        group = self.request.query_params.get('group', None)
        subgroup = self.request.query_params.get('subgroup', None)
        active = self.request.query_params.get('active', None)

        if group is not None:
            queryset = queryset.filter(group=group)
        if subgroup is not None:
            queryset = queryset.filter(subgroup=subgroup)
        if active is not None:
            queryset = queryset.filter(active=active == 'true')

        return queryset.order_by('order')


class ResponseViewSet(viewsets.ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get_queryset(self):
        queryset = Response.objects.all()
        user = self.request.query_params.get('user', None)
        group = self.request.query_params.get('group', None)
        subcategory = self.request.query_params.get('subcategory', None)

        if user is not None:
            queryset = queryset.filter(user=user)
        if group is not None:
            queryset = queryset.filter(group=group)
        if subcategory is not None:
            queryset = queryset.filter(subcategory=subcategory)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)