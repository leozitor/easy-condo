from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.core.exceptions import ValidationError

from webapp.models import *


class GenerateCodeForm(forms.Form):
    codes_qt = forms.IntegerField(label='Codes Quantity', min_value=1, max_value=1000)


class CodeForm(forms.Form):
    code = forms.CharField(max_length=36)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    # # A custom empty label with string
    # date_of_birth = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'date_of_birth', 'gender')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CondoCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    class Meta:
        model = Condo
        fields = ('name', 'address')


class PrettyAuthenticationForm(AuthenticationForm):
    class Meta:
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin', 'condo')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'condo')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class GymSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'checkin_code', 'session_datetime', 'booked_user', 'booking_status')

    def get_user(self, obj):
        return obj.booked_user.user.username

    get_user.short_description = 'username'
    get_user.admin_order_field = 'user__username'


class StallAdmin(admin.ModelAdmin):
    list_display = ('id', 'stall_label', 'condo', 'stall_type')


class StallReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'stall', 'user', 'date')


class TennisCourtAdmin(admin.ModelAdmin):
    list_display = ('id', 'court_number', 'condo', 'time_slot')


class TennisCourtReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'court', 'user', 'date')


class PartyRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'condo')


class PartyRoomReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'party_room', 'user', 'date')


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
admin.site.register(GymSession, GymSessionAdmin)
admin.site.register(Stall, StallAdmin)
admin.site.register(StallReservation, StallReservationAdmin)
admin.site.register(TennisCourt, TennisCourtAdmin)
admin.site.register(TennisCourtReservation, TennisCourtReservationAdmin)
admin.site.register(PartyRoom, PartyRoomAdmin)
admin.site.register(PartyRoomReservation, PartyRoomReservationAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
