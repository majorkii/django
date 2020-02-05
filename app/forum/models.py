from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from time import time


def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))


class Post(models.Model):
	title = models.CharField('Заголовок поста', max_length=100)
	tag = models.CharField(max_length=10, null=True, blank=True)
	slug = models.SlugField('Slug', blank = True, unique = True)
	body = models.TextField('Текст поста')
	created_data = models.DateTimeField('Дата создания', auto_now_add=True)
	author = models.ForeignKey(User, null = True, blank=True, on_delete=models.CASCADE)
	tags = models.ManyToManyField('Tag', related_name='posts', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug})

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	


	def __str__(self):
		return self.title


class Tag(models.Model):
	title = models.CharField('Заголовок тега', max_length=10)
	slug = models.SlugField(max_length=10, unique=True)


	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug':self.slug})

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, null=True, blank=True, related_name='comments', on_delete=models.CASCADE)
	author = models.ForeignKey(User, null = True, blank=True, on_delete=models.CASCADE)
	body = models.TextField('Текст комментария')
	created_data = models.DateTimeField('Дата создания', auto_now_add=True)
	
	def __str__(self):
		return self.body
