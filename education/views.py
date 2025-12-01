from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class CourseViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        qs = Course.objects.filter(deleted_at__isnull=True)
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            if is_active.lower() == "true":
                qs = qs.filter(is_active=True)
            elif is_active.lower() == "false":
                qs = qs.filter(is_active=False)
        return qs


    def list(self, request):
        qs = self.get_queryset(request)
        ser = CourseSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)

    
    def create(self, request):
        ser = CourseSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        ser = CourseSerializer(course, context={"request": request})
        return Response(ser.data)

    
    def update(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        ser = CourseSerializer(course, data=request.data, partial=False, context={"request": request})
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        with transaction.atomic():
            for l in course.lessons.filter(deleted_at__isnull=True):
                l.delete()
            course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    def activate(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if course.is_active:
            return Response({"detail": "Already active."}, status=400)
        course.is_active = True
        course.save(update_fields=["is_active"])
        return Response(CourseSerializer(course, context={"request": request}).data)

    
    def deactivate(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        if course.owner != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if not course.is_active:
            return Response({"detail": "Already inactive."}, status=400)
        course.is_active = False
        course.save(update_fields=["is_active"])
        return Response(CourseSerializer(course, context={"request": request}).data)

    
    def lessons(self, request, pk=None):
        course = get_object_or_404(
            self.get_queryset(request), pk=pk
        )
        lessons = course.lessons.filter(deleted_at__isnull=True).order_by("order")
        ser = LessonSerializer(lessons, many=True)
        return Response(ser.data)

        class LessonViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lesson.objects.filter(deleted_at__isnull=True).select_related("course", "course__owner")

    # helper
    def _get_owned_lesson(self, request, pk):
        lesson = get_object_or_404(self.get_queryset(), pk=pk)
        if lesson.course.owner != request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only course owner allowed.")
        return lesson

    # 3.1 CREATE
    def create(self, request):
        ser = LessonSerializer(data=request.data, context={"request": request})
        if ser.is_valid():
            course = ser.validated_data["course"]
            if course.owner != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            lesson = ser.save()
            return Response(LessonSerializer(lesson).data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    # 3.2 MOVE
    def move(self, request, pk=None):
        before_id = request.data.get("before_lesson_id", None)
        lesson = self._get_owned_lesson(request, pk)
        course = lesson.course

        with transaction.atomic():
            lessons = list(
                course.lessons.filter(deleted_at__isnull=True).order_by("order")
            )
            # normalize orders 10,20,...
            for i, l in enumerate(lessons, start=1):
                l.order = Decimal(i * 10)
                l.save(update_fields=["order"])

            lessons = list(
                course.lessons.filter(deleted_at__isnull=True).order_by("order")
            )

            if before_id is None:
                last = lessons[-1]
                lesson.order = last.order + Decimal("10")
                lesson.indentation = 0
            else:
                before = get_object_or_404(
                    Lesson,
                    id=before_id,
                    course=course,
                    deleted_at__isnull=True,
                )
                # place lesson before "before"
                orders = [l for l in lessons if l.id != lesson.id]
                pos = [i for i, l in enumerate(orders) if l.id == before.id][0]
                # simple: set order = before.order - 5
                lesson.order = before.order - Decimal("5")
                # indentation: one deeper than before (max 5)
                lesson.indentation = min(before.indentation + 1, 5)

            lesson.save(update_fields=["order", "indentation"])

        return Response(
            {"new_order": str(lesson.order), "indentation": lesson.indentation}
        )

    # 3.3 DELETE
    def destroy(self, request, pk=None):
        lesson = self._get_owned_lesson(request, pk)
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def publish(self, request, pk=None):
        lesson = self._get_owned_lesson(request, pk)
        if lesson.is_published:
            return Response({"detail": "Already published."}, status=400)
        lesson.is_published = True
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)
    def unpublish(self, request, pk=None):
        lesson = self._get_owned_lesson(request, pk)
        if not lesson.is_published:
            return Response({"detail": "Already unpublished."}, status=400)
        lesson.is_published = False
        lesson.save(update_fields=["is_published"])
        return Response(LessonSerializer(lesson).data)

