from django.urls import path, include
from .views import Index, DetailArticleView, LikeArticle, Featured, DeleteArticleView, ArticlesByCategory, SearchView, CommentArticle

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', Index.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('<int:pk>/comment', CommentArticle.as_view(), name='comment_article'),
    path('sortBy/title/', SearchView.as_view(), {'order_by': 'title'}, name='sortBy_title'),
    path('sortBy/created_by/', SearchView.as_view(), {'order_by': 'date'}, name='sortBy_created_by'),
    path('sortBy/likes/', SearchView.as_view(), {'order_by': 'likes'}, name='sortBy_likes'),
    path('category/<str:category>/', ArticlesByCategory.as_view(), name='articals_by_categories'),
    path('<int:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('<int:pk>/like', LikeArticle.as_view(), name='like_article'),
    path('featured/', Featured.as_view(), name='featured'),
    path('<int:pk>/delete', DeleteArticleView.as_view(), name='delete_article'),
]