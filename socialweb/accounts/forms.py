from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UsernameField

class CustomUserCreateForm(UserCreationForm):
	class Meta:
		model=CustomUser
		fields=(
			'username',
			'email',
			'password1',
			'password2',
			'user_image',
		)
		field_classes={'username': UsernameField}

class UpdateUserProfileForm(forms.ModelForm):
	class Meta:
		model=CustomUser
		fields=(
			'user_image',
			'user_description'
		)