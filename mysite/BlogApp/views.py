from django.contrib.syndication.views import Feed
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy

from .models import Article


class BasedView(ListView):
    """
    Представление для отображения списка статей.
    """

    template_name = "blogapp/article_list.html"
    context_object_name = 'articles'
    queryset = (Article.objects.
                select_related('author', 'category').
                prefetch_related('tags').
                defer("content").
                all()
                )


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(pub_date__isnull=False)
        .order_by("-pub_date")
    )


class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on changes and addition blog articles"
    link = reverse_lazy("BlogApp:article_list")

    def items(self):
        return (Article.objects.
                filter(pub_date__isnull=False)
                .order_by('-pub_date').defer("content")
                .select_related('author', 'category').prefetch_related('tags')[:5]
                )

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]

    