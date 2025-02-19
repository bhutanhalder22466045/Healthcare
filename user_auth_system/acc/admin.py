from django.contrib import admin
from .models import CustomUser  # Import your user model


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


admin.site.register(CustomUser, CustomUserAdmin)