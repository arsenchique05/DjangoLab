from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from education.views import CourseViewSet, LessonViewSet

course_list = CourseViewSet.as_view({
    "get": "list",
    "post": "create",
})
course_detail = CourseViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "delete": "destroy",
})
course_activate = CourseViewSet.as_view({"post": "activate"})
course_deactivate = CourseViewSet.as_view({"post": "deactivate"})
course_lessons = CourseViewSet.as_view({"get": "lessons"})

lesson_create = LessonViewSet.as_view({"post": "create"})
lesson_move = LessonViewSet.as_view({"put": "move"})
lesson_delete = LessonViewSet.as_view({"delete": "destroy"})
lesson_publish = LessonViewSet.as_view({"post": "publish"})
lesson_unpublish = LessonViewSet.as_view({"post": "unpublish"})

schema_view = get_schema_view(
    title="Education API",
    description="Courses & Lessons",
    version="1.0.0",
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # 1. JWT
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),

    # 2. COURSES
    path("api/v1/education/courses/", course_list),
    path("api/v1/education/courses/<int:pk>/", course_detail),
    path("api/v1/education/courses/<int:pk>/activate/", course_activate),
    path("api/v1/education/courses/<int:pk>/deactivate/", course_deactivate),
    path("api/v1/education/courses/<int:pk>/lessons/", course_lessons),

    # 3. LESSONS
    path("api/v1/education/lessons", lesson_create),
    path("api/v1/education/lessons/<int:pk>/move", lesson_move),
    path("api/v1/education/lessons/<int:pk>/", lesson_delete),
    path("api/v1/education/lessons/<int:pk>/publish/", lesson_publish),
    path("api/v1/education/lessons/<int:pk>/unpublish/", lesson_unpublish),

    # DOCS
    path("api/schema/", schema_view, name="api-schema"),
    path("api/docs/", include_docs_urls(title="Education API")),
]
