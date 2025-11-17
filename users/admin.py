from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser

class CustomerUserAdmin(UserAdmin):
    model=CustomerUser
    list_display=('email','username','first_name','last_name','department','role','is_staff')
    ordering=('email',)
    search_fields=('email','username','first_name','last_name')

    fieldsets=(
        (None, {"fields":("email","password")}),
        ("Personal info", {"fields":("username","first_name","last_name","phone","city","country","department","role","birth_date","salary")}),
        ("Permissions", {"fields":("is_active","is_staff","is_superuser","groups","user_permissions")}),
        ("Important", {"fields":("last_login","date_joined")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )


admin.site.register(CustomerUser, CustomerUserAdmin)