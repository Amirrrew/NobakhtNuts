from django.http import HttpRequest
from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import View, TemplateView, ListView

from userpanel_module.views import MyTickets
from .form import NewTicketForm
from support_module.models import SupportWays, TicketReason, Ticket, TicketStatus, QuestionCategory


class SupportView(ListView):
    template_name = 'support_module/contact_us.html'
    model = SupportWays
    context_object_name = 'support'

# class SupportView(View):
#     def get(self, request):
#         support = SupportWays.objects.all()
#         ticket_form = NewTicketForm()
#         ticket_reasons = TicketReason.objects.all()
#         questions = QuestionCategory.objects.prefetch_related('question_set')
#         context = {
#             'support': support,
#             'ticket_form': ticket_form,
#             'ticket_reasons': ticket_reasons,
#             'questions': questions,
#         }
#         return render(request ,'support_module/contact_us.html', context)
#
#
#     def post(self ,request: HttpRequest):
#         support = SupportWays.objects.all()
#         ticket_form = NewTicketForm(request.POST ,request.FILES)
#         ticket_reasons = TicketReason.objects.all()
#         questions = QuestionCategory.objects.prefetch_related('question_set')
#         message = None
#         message_e = None
#         popup_open = None
#         try:
#             if request.user.is_authenticated:
#                 if ticket_form.is_valid():
#                     title = ticket_form.cleaned_data.get('title')
#                     reason_selected = request.POST.get('reason')
#                     text = ticket_form.cleaned_data.get('text')
#                     image = request.FILES.get('image')
#
#                     reason = TicketReason.objects.filter(id=reason_selected).first()
#                     status = TicketStatus.objects.get(id=1)
#
#                     if not title:
#                         message_e = 'برای تیکت یک عنوان بنویسید'
#                     if not text:
#                         message_e = 'مشکل خود را شرح دهید'
#                     else:
#                         new_ticket = Ticket(
#                             title=title,
#                             reason=reason,
#                             text=text,
#                             status=status,
#                             user=request.user,
#                         )
#                         if image:
#                             new_ticket.img = image
#                         new_ticket.save()
#                         message = 'تیکت با موفقیت ارسال شد!'
#                 else:
#                     message_e = 'تمام فیلد هارا به درستی پر کنید'
#                     popup_open = True
#             else:
#                 message_e = 'برای ارسال تیکت ابتدا باید وارد شوید'
#         except:
#             message_e = 'مشکلی در ارسال تیکت پیش آمده!'
#             popup_open = True
#
#         context = {
#             'ticket_form': ticket_form,
#             'message': message,
#             'message_e': message_e,
#             'ticket_reasons': ticket_reasons,
#             'popup_open': popup_open,
#             'support': support,
#             'questions': questions
#         }
#         return render(request, 'support_module/contact_us.html', context)
#

