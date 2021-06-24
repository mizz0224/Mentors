import os
from django.views.generic import TemplateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from users import models

# Create your views here.
class HomeView(ListView):
    model = models.Mentor
    template_name = "home.html"
    context_object_name = "Mentors"
    paginate_by = 10
    def get_queryset(self):
        return models.Mentor.objects.filter(is_authorized=True)
        
def search_mentor(request):
    # get_name = request.GET.get("name")
    get_name = request.POST.get("name")
    if get_name == "":
        return redirect(reverse("core:home"))
    # 안에 변수는 짧게하는게 좋음
    obj = (
        models.Mentor.objects.filter(user__name__icontains=get_name)
        | models.Mentor.objects.filter(main_branch__name__icontains=get_name)
        | models.Mentor.objects.filter(sub_branch__name__icontains=get_name)
    ).filter(is_authorized=True)
    #obj = searched_obj.
    #obj = searched_obj.objects.filter(is_authorized=True)
    # 포함관계설정
    # obj = models.Mentor.objects.all()
    # return redirect(reverse())
    if get_name:
        return render(
            request, "home.html", {"mentors": obj, "get_name": get_name, "searched" : True}
        )
    else:
        return render(request, "home.html",{"searched" : True})
    # pass