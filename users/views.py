from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from django.contrib.auth import logout
from django import forms
from django.contrib.auth.models import User

from blog.models import Article

class RegisterView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect('index')

class ProfileView(View):
	def get(self, request):
		form = UserUpdateForm(instance=request.user)

		return render(request, 'users/user-profile.html', {
			'title': 'Profile  - Everything Of Life',
			'form': form
		})

	def post(self, request):
		if request.method == 'POST':
			form = UserUpdateForm(request.POST, instance=request.user)
			if form.is_valid():
				form.save()
				return redirect('/account/profile/')
		else:
			form = UserUpdateForm(instance=request.user)

		return render(request, 'users/user-profile.html', {
			'title': 'Profile  - Everything Of Life',
			'form': form
		})

class PostCollectionView(View):
	def get(self, request):

		user_id = request.user.id
		articles = Article.objects.filter(author_id=user_id)

		context = {
			'title': 'Post Collection  - Everything Of Life',
			'articles': articles
		}

		return render(request, 'users/post-collection.html', context)

def delete_article(request, article_id):
    # Get the article instance using get_object_or_404
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        # Check if the user has permission to delete the article (optional)
        if request.user == article.author:
            # Delete the article
            article.delete()
            return redirect('list_articles')  # Redirect to a view showing the list of articles
        else:
            # Handle unauthorized deletion (optional)
            return render(request, 'unauthorized_delete.html')

    context = {
        'article': article,
    }

    return render(request, 'users/post-collection.html', context)

def logout_user (request):
	logout(request=request)
	return redirect('/')
