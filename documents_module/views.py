from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from support_module.models import QuestionCategory


class About_us(TemplateView):
    template_name = 'documents_module/about_us.html'

class FAQ(ListView):
    model = QuestionCategory
    template_name = 'documents_module/faq.html'
    context_object_name = 'questions'

    def get_queryset(self):
        return QuestionCategory.objects.prefetch_related('question_set')