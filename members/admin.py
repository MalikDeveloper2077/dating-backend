from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Member


class MemberAdmin(UserAdmin):
    search_fields = ('name', 'surname', 'email')
    list_display = ('id', 'email', 'name', 'surname')
    list_display_links = ('id', 'email')
    list_filter = ('sex',)
    ordering = ('id',)
    fieldsets = (
        ('Авторизация', {'fields': ('email', 'password')}),
        ('Информация', {'fields': ('name', 'surname', 'sex', 'photo',
                                   'liked_members', 'longitude', 'latitude')})
    )


admin.site.register(Member, MemberAdmin)
