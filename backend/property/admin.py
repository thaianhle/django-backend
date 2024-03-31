from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Property
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class PropertyAdmin(admin.ModelAdmin):

    #fieldsets = (
    #    (None, {'fields': ('title', 'id', 'lanlord')}),
    #    #('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #)

    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        v = super().get_queryset(request).select_related(
            'landlord'
        ).only('landlord__first_name', 'landlord__last_name')
        return v
    
    def owner(self, obj):
        l = obj.landlord
        return f'{l.avatar_image()}'
    
    # list_display only understand attribute or method
    # if you want select related field on model related
    # then write custom method return field name in model related
    list_display = (
        'title',
        'id',
        'owner',
    )

    


    #list_select_related = ['landlord__email']
    #list_select_related = (
        #'landlord__name',
    #    'landlord__email',
    #)


    pass
admin.site.register(Property, PropertyAdmin)
