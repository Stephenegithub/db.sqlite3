from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import UserCreationForm

# Register your models here.


admin.site.unregister(Group)
admin.site.site_header = "Smart Chick Farm Admin"
admin.site.site_name = "Smart Chick Farm Admin"
admin.site.site_title = "Smart Chick Farm Admin"
admin.site.index_title = "Smart Chick Farm Admin"


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_staff')
    search_fields = ('email', 'is_admin')
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )


admin.site.register(CustomUser, AccountAdmin)