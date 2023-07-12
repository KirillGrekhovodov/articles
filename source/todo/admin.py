from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from todo.models import Type, Status, Todo


# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    filter_horizontal = ('types',)


admin.site.register(Todo, TodoAdmin)
admin.site.register(Type)
admin.site.register(Status)
