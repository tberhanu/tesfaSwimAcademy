from django.contrib import admin
from .models import User, UserRequest

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone', 'country', 'city')
    list_filter = ('country', 'city')
    search_fields = ('email', 'name', 'phone')
    readonly_fields = ('email',)

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
