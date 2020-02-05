from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
	

	def save(self, *args, **kwargs):
		form = CommentForm(request.POST)
		if form.is_valid():
			post = Post.objects.create(
				title=self.cleaned_data['title'],
				body=self.cleaned_data['bods'],
				tags=self.cleaned_data['tags'],
				)
			
	
			


	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()

		if new_slug == 'create':
			raise ValidationError('Нельзя создать тег "Create"')
		return new_slug


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title', 'slug']

		widgets = {
			'title' : forms.TextInput(attrs={'class': 'form-control'}),
			'slug' : forms.TextInput(attrs={'class': 'form-control'}),
				}

	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()
		if new_slug == 'create':
			raise ValidationError('Нельзя создать тег "Create"')
		if Tag.objects.filter(slug__iexact=new_slug).count():
			raise ValidationError('Такой тег {} уже существует, попробуйте другой'.format(new_slug))
		return new_slug

	def save(self):
		new_tag = Tag.objects.create(
			title=self.cleaned_data['title'],
			slug=self.cleaned_data['slug']
			)
		return new_tag


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'