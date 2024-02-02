from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (User, Profile)
from .forms import UserAdminCreationForm, UserAdminChangeForm


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    inlines = (ProfileInline,)
    list_display = ('id', 'suid', 'full_name', 'phone_number', 'email',
                    'is_staff', 'is_guest')
    search_fields = ('suid',  'full_name', 'phone_number',)
    list_filter = ('is_staff', 'is_guest')
    readonly_fields = ('id', 'suid', 'is_guest', 'avatar_tag')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'is_phone_number_verified',  'email', 'is_email_verified','avatar', 'avatar_tag')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_guest')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )
    ordering = ('id',)
    filter_horizontal = ()

    # def get_inline_instances(self, request, obj=None):
    #     if not obj:
    #         return list()
    #     return super(UserAdmin, self).get_inline_instances(request, obj)


admin.site.register(User, UserAdmin)


admin.site.site_header = 'Starter'
admin.site.site_title = 'Security Center'
admin.site.index_title = 'Starter'