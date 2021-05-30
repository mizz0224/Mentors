import datetime
from django.http import Http404
from django.views.generic import View, ListView
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from users import models as user_models
from reviews import forms as reviews_forms
from django.db.models import Q
from . import models

# Create your views here.

class CreateError(Exception):
    pass

def create(request, mentor, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        mentor = user_models.Mentor.objects.get(pk=mentor)
        models.BookedDay.objects.get(day=date_obj, reservation__mentor=mentor)
        raise CreateError()
    except (user_models.Mentor.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Mentor")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        user = request.user
        ckr = models.Reservation.objects.get_or_none(
            user=user,
            mentor=mentor,
            check_in=date_obj,
        )
        if ckr is None:
            reservation = models.Reservation.objects.create(
                user=request.user,
                mentor=mentor,
                check_in=date_obj,
                check_out=date_obj,
            )
            return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
        return redirect(reverse("reservations:detail", kwargs={"pk": ckr.pk}))
class ReservationDetailView(View):
    
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        user = self.request.user
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if reservation is None or (not (reservation.user == user or reservation.mentor.user == user)):
            return redirect(reverse("core:home"))
        form = reviews_forms.CreateReviewForm()
        return render(self.request, "reservations/detail.html", {"reservation":reservation, "form":form})

def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    # if reservation is None or (reservation.user != request.user or reservation.mentor.user != request.user):
    #    raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
    # return redirect(reverse("reservations:list", kwargs={"pk": reservation.pk}))

class ReservationListView(ListView):

    paginate_by = 10
    # paginate_orphans = 5
    context_object_name = "reservations"
    
    def get_queryset(self):
        
        user = self.request.user
        
        if user.is_mentor:
            qs = models.Reservation.objects.filter(mentor__user=user)
        else:
            qs = models.Reservation.objects.filter(user=user)
        return qs