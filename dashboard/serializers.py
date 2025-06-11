# dashboard/serializers.py
from rest_framework import serializers
from .models import Group, Category, Subcategory, ChecklistQuestion, Response


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'parent']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class SubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Subcategory
        fields = ['id', 'title', 'category', 'category_name']


class ChecklistQuestionSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.title', allow_null=True)
    subgroup_name = serializers.ReadOnlyField(source='subgroup.title', allow_null=True)

    class Meta:
        model = ChecklistQuestion
        fields = ['id', 'question_text', 'order', 'active', 'active_system',
                  'group', 'group_name', 'subgroup', 'subgroup_name', 'created_at']


class ResponseSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Response
        fields = ['id', 'user', 'username', 'question', 'answer', 'group',
                  'subcategory', 'created_at', 'file', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None