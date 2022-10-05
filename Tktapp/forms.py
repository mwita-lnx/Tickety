from dataclasses import fields
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField,PasswordChangeForm
from .models import *

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','full_name'] 

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")

        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
   

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = '__all__'

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Categories
		fields = '__all__'

class Ticketform(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'


CategoryInlineFormset = inlineformset_factory(
    Event,
    Categories,
    form=CategoryForm,
    extra=5,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

TicketInlineFormset = inlineformset_factory(
    Event,
    Ticket,
    form= Ticketform,
    extra=1,
    # max_num=5,
    # fk_name=None,
    # fields=None, exclude=None, can_order=False,
    # can_delete=True, max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)

class PasswordChangeCustomForm(PasswordChangeForm):
    pass

    