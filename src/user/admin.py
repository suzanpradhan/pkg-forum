from django import forms
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from src.user.forms import CustomUserChangeForm, CustomUserCreationForm
from src.user.models import Profile, User


class CustomUserAdmin(UserAdmin):
    """Customer User Admin Configuration"""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "id",
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "profile", "is_active")}),
        ("Permissions", {"fields": ("is_staff",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class GroupAdminForm(forms.ModelForm):
    """Group Admin Form"""

    users = forms.ModelMultipleChoiceField(
        User.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple("Users", False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list("pk", flat=True)
            self.initial["users"] = initial_users

    def save(self, *args, **kwargs):
        kwargs["commit"] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)

    # pylint: disable=method-hidden
    # pylint: disable=missing-function-docstring
    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data["users"])


class CustomGroupAdmin(GroupAdmin):
    """Custom Group Admin"""

    form = GroupAdminForm


admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
