from django.db import models
from decimal import Decimal
from django.conf import settings
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    owner= models.ForeignKey (
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_courses",
    )
    deleted_at=models.DateTimeField(null=True,blank=True)

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return self.title

    class Lesson(models.Model):
        course= models.ForeignKey(
            Course,
            on_delete=models.CASCADE,
            related_name="lessons",
        )
        title= models.CharField(max_length=255)
        content= models.TextField()
        order=models.DecimalField(max_digits=7, decimal_places=2)
        indentation= models.positivesmallinteger(default=0)
        is_published= models.BooleanField(default=False)
        created_at= models.DateTimeField(auto_now_add=True)
        updated_at= models.DateTimeField(auto_now=True)
        deleted_at=models.DateTimeField(null=True,blank=True)

        def delete(self, *args, **kwargs):
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at"])

        def __str__(self):
            return self.title
            
            
            