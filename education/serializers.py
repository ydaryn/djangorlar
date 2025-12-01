from rest_framework import serializers
from .models import Course, Lesson
from django.db.models import Min
from decimal import Decimal

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'order', 'created_at', 'updated_at', 'is_published', 'indentation']
        read_only_fields = ['id', 'created_at', 'updated_at', 'order']

        def create(self, validated_data):
            course = validated_data['course']
            min_order = course.lessons.filter(deleted_at__isnull = True).aggregate(min_order=Min('order'))['min_order']
            if min_order is None:
                new_order = Decimal('0')
            else:
                new_order = min_order - Decimal('1')
            
            validated_data['order'] = new_order
            return super().create(validated_data)
        
class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_active', 'created_at', 'updated_at', 'owner', 'lessons_count'],
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner',]

        def get_lessons_count(self, obj):
            return obj.lessons.filter(deleted_at__isnull=True).count()
        
        def create(self, validated_data):
            user = getattr(request, 'user', None)
            validated_data['owner'] = user
            request = self.context.get('request')
            return super().create(validated_data)

        def update(self, instance, validated_data):
            validated_data.pop('owner', None)
            return super().update(instance, validated_data)
        
