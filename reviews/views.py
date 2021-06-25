from django.contrib import messages
from django.views.generic import UpdateView, ListView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.db.models import Q
from users import models as user_models
from . import models, forms

# Create your views here.
def create_review(request, mentor):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        mentor = user_models.Mentor.objects.get_or_none(pk=mentor)
        if not mentor:
            return redirect(reverse("core:home"))
        if form.is_valid():
            review = form.save()
            review.mentor = mentor
            review.user = request.user
            review.save()
            messages.success(request, "Mentor reviewed")
            return redirect(reverse("users:detail", kwargs={'pk':mentor.pk}))
        
class Update_review(UpdateView):
    model = models.Review
    context_object_name = 'review'
    template_name = "reviews/update-review.html"
    fields = (
        "score",
        "review",
    )
    success_message = "Review updated"
    
    def get_object(self, queryset=None):
        pk = self.kwargs["pk"]
        review = models.Review.objects.get(pk=pk)
        return review

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['score'].widget.attrs ={"label" :"Score",'placeholder': "score", 'class' :"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded" }
        form.fields['review'].widget.attrs ={"label" :"Review",'placeholder': "review", 'class' :"w-full px-5 py-1 text-gray-700 bg-gray-200 rounded"  }
        return form
    
    def get_success_url(self):
        review_pk = self.kwargs['pk']
        review = models.Review.objects.get(pk=review_pk)
        mentor = review.mentor
        return reverse_lazy("users:detail", kwargs={'pk':mentor.pk})
    
def remove_review(self, pk):
    review = models.Review.objects.get(pk=pk)
    review.review = "삭제된 메시지입니다"
    review.save()
    return redirect(reverse("users:detail", kwargs={'pk':review.mentor.pk}))