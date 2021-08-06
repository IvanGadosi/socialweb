from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=(
			'title',
			'description',
			'post_image',
			'creator',
			'category'
		)
		widgets = {'creator': forms.HiddenInput()}


class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=(
			'comment_text',
			'comment_user',
			'comment_post'
		)
		widgets = {'comment_user': forms.HiddenInput(),
		'comment_post': forms.HiddenInput(),
		'comment_text': forms.Textarea(attrs={'rows':3,})}