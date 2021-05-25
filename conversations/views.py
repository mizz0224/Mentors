from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from users import models as user_models
from . import models, forms
# Create your views here.


def go_conversation(requset, user_pk, mentor_pk):
    user = user_models.User.objects.get(pk=user_pk)
    mentor = user_models.Mentor.objects.get(pk=mentor_pk)
    if user is not None and mentor is not None:
        try:
            conversation = models.Conversation.objects.get(Q(user=user) & Q(mentor=mentor))
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create(
                user = user,
                mentor = mentor,
            )
        return redirect(reverse("conversations:detail", kwargs={'pk':conversation.pk}))
    
class ConversationDetailView(View):
    
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get(pk=pk)
        if not conversation:
            raise Http404()
        return render(self.request, "conversations/conversation_detail.html", {"conversation":conversation})
    
    def post(self, *args, **kwargs):
        message = self.request.POST.get('message', None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={'pk':pk}))
        