from django.shortcuts import render
from django.views.generic import ListView, DetailView

from article_module.models import Article
from product_module.models import Product
from django.db.models import F


class ArticleListView(ListView):
    model = Article
    template_name = 'article_module/article_grid.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        return Article.objects.filter(is_active=True)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        article = self.object
        Article.objects.filter(pk=article.pk).update(view=F('view')+1)
        context = super(ArticleDetailView ,self).get_context_data(**kwargs)
        context['most_viewed_articles'] = Article.objects.filter(is_active=True).exclude(id=article.id).order_by('-view')[:4]
        context['recent_products'] = Product.objects.filter(is_active=True ,is_deleted=False ,quantity__gt=0).order_by('created_at')[:6]
        return context

