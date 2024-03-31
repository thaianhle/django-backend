from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm
# Register your models here.
#from .models import User
#admin.site.register(User)
 
class CustomUserAdminCreate(forms.ModelForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput)
    password2=forms.CharField(label='Comfirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'avatar')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class CustomUserAdmin(UserAdmin, ModelAdmin):
    
    #print(UserAdmin.fieldsets)
    #form = CustomUserAdminChange
    add_form = CustomUserAdminCreate
    change_password_form = AdminPasswordChangeForm
    #readonly_fields = ('avatar_url',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'avatar', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    print(UserAdmin.add_fieldsets)
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'avatar', 'is_staff', 'is_superuser'),
        }),
    )

    list_display = (
        #'avatar_image',
        "id",
        "email",
        'date_joined',
        #"Permission"
    )

    search_fields = (
        "email",
        'date_joined'
    )

    #autocomplete_fields = (
    #    "id",
    #)

    ordering = ['email']

#admin.site.unregister()
admin.site.register(User, CustomUserAdmin)

