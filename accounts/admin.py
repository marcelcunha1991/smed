from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Cargo
from .forms import UserCreationForm, UserAdminForm


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'cargo', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'cargo')
        }),
        ('Informações Básicas', {
            'fields': ('name', 'phone', 'last_login')
        }),
        ('Permissões', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_logged', 'groups',
                'user_permissions'
            )
        }
         ),
    )
    list_display = ['username', 'name', 'phone', 'email', 'is_active', 'is_staff', 'date_joined']


admin.site.register(User, UserAdmin)
admin.site.register(Cargo)
