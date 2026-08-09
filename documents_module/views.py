from django.shortcuts import render
from django.template.defaultfilters import title
from django.views.generic import TemplateView, ListView

from support_module.models import QuestionCategory, SupportWays


class About_us(TemplateView):
    template_name = 'documents_module/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(About_us ,self).get_context_data(**kwargs)
        context['insta'] = SupportWays.objects.filter(title='اینستاگرام').first()
        return context

class FAQ(ListView):
    model = QuestionCategory
    template_name = 'documents_module/faq.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return QuestionCategory.objects.prefetch_related('question_set')


class Policies(TemplateView):
    template_name = 'documents_module/policies.html'

class BulkBuy(TemplateView):
    template_name = 'documents_module/bulk-buy.html'
