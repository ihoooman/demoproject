from django.db import models
from django.conf import settings


class Group(models.Model):
    title = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.title


class ChecklistQuestion(models.Model):
    QUESTION_TYPES = (
        ('TEXT', 'Text Response'),
        ('FILE', 'File Upload'),
    )

    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='TEXT')
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='checklist_questions')
    # Add this new field
    subgroup = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='subgroup_checklist_questions')
    SYSTEM_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    active_system = models.CharField(max_length=5, choices=SYSTEM_CHOICES)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text

    class Meta:
        permissions = [
            ("manage_checklist_settings", "Can manage checklist settings"),
        ]

class SubcategoryResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s response to {self.subcategory.title}"


class Response(models.Model):
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='responses', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    file = models.FileField(upload_to='responses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s response for {self.question}"