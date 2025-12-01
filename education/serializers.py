from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.models import get_user_model
from .models import Course, Lesson

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class CourseSerializer(serializers.ModelSerializer):
    owner= usershortserializer(read_only=True)
    lesson_count= serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ["id", "title", "description", "is_active", "created_at", "updated_at", "owner", "lesson_count","deleted_at"]
        read_only_fields = ["id","created_at", "updated_at", "deleted_at","owner","lesson_count"]

    def get_lesson_count(self, obj):
        return obj.lessons.filter(deleted_at__isnull=True).count()

        def create(self, validated_data):
            request = self.context.get("request")
            validated_data["owner"] = request.user
            return super().create(validated_data)

        def update(self, instance, validated_data):
            class Meta:
                model = Lesson
                fields=['id','course','title','description','order','indentation','is_published','created_at','updated_at','deleted_at']
                read_only_fields=['id','course','order','created_at','updated_at','deleted_at']
                def create(self, validated_data):

                    request = self.context.get("request")
                    course_id= request.query_params.get("course_id")
                    if not course_id:
                        raise serializers.ValidatationError(f"{course_id} is required")

                        from .models import Course
                        try:
                            course = Course.objects.get(id=course_id,deleted_at__isnull=True)
                        except Course.DoesNotExist:
                            raise serializers.ValidatationError(f"{course_id} is not found")
                        except Course.MultipleObjectsReturned:
                        validated_data["course"] = course
                        qs=course.lessons.filter(deleted_at__isnull=True).order_by("order")
                        if qs.exists():
                            top_order=qs.last().order
                            validated_data["order"]=top_order-decimal('10.0')
                        else:
                                validateed_data['indentation']=decimal('0')
                                validated_data['order']=decimal('0')
                        return super().create(validated_data)
                        
