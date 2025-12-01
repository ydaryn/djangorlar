from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Max
from decimal import Decimal
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs=Course.objects.all()
        is_active=self.request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() in ['true', '1']:
                qs = qs.filter(is_active=True)
            else:
                qs = qs.filter(is_active=False)
        return qs
    
    def list(self, request):
        qs = self.get_queryset().annotate(lesson_count=Count('lessons', filter=Q(lessons__deleted_at__isnull=True)))
        serializer = CourseSerializer(qs, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = CourseSerializer(data = request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.owner != request.user:
            return Response({'detail': 'You do not have permission to edit this course.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = CourseSerializer(course, data = request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(CourseSerializer(course).data)
    
    def destroy (self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this course.'}, status=status.HTTP_403_FORBIDDEN)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='activate')
    def activate(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.owner != request.user:
            return Response({'detail': 'You do not have permission to activate this course.'}, status=status.HTTP_403_FORBIDDEN)
        if course.is_active:
            return Response({'detail': 'Course is already active.'}, status=status.HTTP_400_BAD_REQUEST)
        course.is_active = True
        course.save(update_fields=['is_active'])
        return Response(CourseSerializer(course).data)
    
    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        if course.owner != request.user:
            return Response({'detail': 'You do not have permission to deactivate this course.'}, status=status.HTTP_403_FORBIDDEN)
        if not course.is_active:
            return Response
        
    @action(detail=True, methods=['get'], url_path='lessons')
    def lessons(self, request, pk=None):
        course = get_object_or_404(Course.objects.all(), pk=pk)
        lessons = course.lessons.filter(deleted_at__isnull=True).order_by('order')
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)
    
        
class LessonViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self,request):
        data = request.data.copy()
        course_id = data.get('course')
        if not course_id:
            return Response({'detail': 'course field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        course = get_object_or_404(Course.objects.all(), pk=course_id)
        if course.owner != request.user:
            return Response({'detail': 'You do not have permission to add lessons to this course.'}, status=status.HTTP_403_FORBIDDEN)
        serializer= LessonSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        lesson = serializer.save()
        return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk=None):
        lesson = get_object_or_404(Lesson.objects.all(), pk=pk)
        if lesson.course.owner != request.user:
            return Response({'detail': 'You do not have permission to delete this lesson.'}, status=status.HTTP_403_FORBIDDEN)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='move')
    def move(self, request, pk=None):
        lesson = get_object_or_404(Lesson.objects.all(), pk=pk)
        if lesson.course.owner != request.user:
            return Response({'detail': 'You do not have permission to move this lesson.'}, status=status.HTTP_403_FORBIDDEN)
        before_id = request.data.get('before_id', None)
        #siblings are non deleted lessons excludin gmoving one
        siblings = Lesson.objects.filter(course=lesson.course, deleted_at__isnull=True).exclude(pk=lesson.pk).order_by('order')
        if before_id is None:
            max_order = siblings.aggregate(max_order = Max('order'))['max_order']
            if max_order is None:
                new_order = Decimal('0')
            else:
                new_order = Decimal(max_order)+Decimal('1')
            lesson.order = new_order
            lesson.indentation = 0
            lesson.save(update_fields=['order', 'indentation'])
            return Response({'order':str(lesson.order)})
        else:
            before = get_object_or_404(Lesson.objects.all(), pk = before_id)
            if before.course_id != lesson.course_id:
                return Response({'detail': 'The before_id lesson must belong to the same course.'}, status=status.HTTP_400_BAD_REQUEST)
            course_lessons=list(siblings.order_by('order'))
            idx=None
            for i , l in enumerate(course_lessons):
                if l.pk == before.pk:
                    idx=i
                    break
            if idx is None:
                course_lessons = list(lesson.course.lessons.filter(deleted_at__isnull=True).order_by('order'))
                for i, l in enumerate(course_lessons):
                    if l.pk == before.pk:
                        idx=i
                        break
            if idx is None:
                return Response({'detail': 'The before_id lesson is not found among the course lessons.'}, status=status.HTTP_400_BAD_REQUEST)
                prev_order = None
                if idx -1>=0:
                    prev_order = course_lessons[idx-1].order
                next_order = course_lessons[idx].order
                if prev_order is None:
                    new_order = Decimal(next_order) - Decimal('1')
                else:
                    new_order = (Decimal(prev_order) + Decimal(next_order)) / Decimal('2')

                new_indentation = min(before.indentation, 5)
                lesson.order = new_order
                lesson.indentation = new_indentation
                lesson.save(update_fields=['order', 'indentation'])
                return Response({'order': str(lesson.order)})
            
    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        lesson = get_object_or_404(Lesson.objects.all(), pk=pk)
        if lesson.course.owner != request.user:
            return Response({'detail': 'Only course owner can publish lesson.'}, status=status.HTTP_403_FORBIDDEN)
        if lesson.is_published:
            return Response({'detail': 'Already published.'}, status=status.HTTP_400_BAD_REQUEST)
        lesson.is_published = True
        lesson.save(update_fields=['is_published'])
        return Response(LessonSerializer(lesson).data)
        
    @action(detail=True, methods=['post'], url_path='unpublish')
    def unpublish(self, request, pk=None):
        lesson = get_object_or_404(Lesson.objects.all(), pk=pk)
        if lesson.course.owner != request.user:
            return Response({'detail': 'Only course owner can unpublish lesson.'}, status=status.HTTP_403_FORBIDDEN)
        if not lesson.is_published:
            return Response({'detail': 'Already unpublished.'}, status=status.HTTP_400_BAD_REQUEST)
        lesson.is_published = False
        lesson.save(update_fields=['is_published'])
        return Response(LessonSerializer(lesson).data)