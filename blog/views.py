from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Article, Category, Comment
from django.db.models import Q, Count

class Index(ListView):
	model = Article
	queryset = Article.objects.all().order_by('-date')
	template_name = 'blog/index.html'
	paginate_by = 6

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

class SearchView(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6
  
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["categories"] = Category.objects.all()
		return context

	def get_queryset(self):
		query = self.request.GET.get('q')
		order_by = self.request.GET.get('order_by', 'title')
			
		if query:
			queryset = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
		else:
			queryset = Article.objects.all()

		if order_by == 'title':
			queryset = queryset.order_by('title')
		elif order_by == 'date':
			queryset = queryset.order_by('date')
		else:
			queryset = queryset.annotate(like_count=Count('likes')).order_by('like_count')
		return queryset

class ArticlesByCategory(ListView):
	model = Article
	template_name = 'blog/index.html'
	paginate_by = 6

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def get_queryset(self, *args, **kwargs):
		return Article.objects.filter(category=self.kwargs.get('category')).order_by('-date')

class Featured(ListView):
	model = Article
	queryset = Article.objects.filter(featured=True).order_by('-date')
	template_name = 'blog/featured.html'
	paginate_by = 6

class DetailArticleView(DetailView):
	model = Article
	template_name = 'blog/detail_post.html'

	def get_context_data(self, *args, **kwargs):
		context = super(DetailArticleView, self).get_context_data(*args, **kwargs)
		context['liked_by_user'] = False
		article = Article.objects.get(id=self.kwargs.get('pk'))
		if article.likes.filter(pk=self.request.user.id).exists():
			context['liked_by_user'] = True
		return context

class LikeArticle(View):
	def post(self, request, pk):
		article = Article.objects.get(id=pk)
		if article.likes.filter(pk=self.request.user.id).exists():
			article.likes.remove(request.user.id)
		else:
			article.likes.add(request.user.id)

		article.save()
		return redirect('detail_article', pk)

class CommentArticle(View):
	def post(self, request, pk):
		comment_text = request.POST.get('comment_text')
		if comment_text:
			article = Article.objects.get(id=pk)
			comment = Comment.objects.create(content=comment_text, user=request.user, article=article)
			article.comments.add(comment)

		return redirect('detail_article', pk)

class DeleteArticleView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Article
	template_name = 'blog/blog_delete.html'
	success_url = reverse_lazy('index')

	def test_func(self):
		article = Article.objects.get(id=self.kwargs.get('pk'))
		return self.request.user.id == article.author.id
	