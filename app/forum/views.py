from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class PostList(ListView):
	model = Post


class PostDetail(DetailView):
	model = Post

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs) # data = {'post':post}
		data['form'] = CommentForm() # data = {'post':post,'form':form}
		return data

	def post(self,request,*args,**kwargs):
		form = CommentForm(request.POST)
		post = self.get_object()

		if form.is_valid():
			comment = Comment(body=form.cleaned_data['body'],post=post,author=request.user)
			comment.save()
			return redirect(post)
		return render(request,'forum/post_detail.html',context={'form':form,'post':post})


class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	fields = '__all__'
		
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class TagList(ListView):
	model = Tag


class TagDetail(DetailView):
	model = Tag


class TagCreate(LoginRequiredMixin, View):
	def get(self,request):
		form = TagForm()
		return render (request, 'forum/tag_form.html', context={'form':form})

	def post(self, request):
		bound_form = TagForm(request.POST)

		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect(new_tag)
		return render (request, 'forum/tag_form.html', context={'form':bound_form})


