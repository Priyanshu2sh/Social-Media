from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'date_of_birth', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('username', 'email', 'name')

admin.site.register(User, UserAdmin)