import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, View

from .models import Submission


class SubmissionListView(LoginRequiredMixin, ListView):
    model = Submission
    template_name = "submits/list.html"
    context_object_name = "submissions"
    paginate_by = 20

    def get_queryset(self):
        qs = Submission.objects.select_related("user", "input_data").order_by("-created_at")
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        return qs.filter(user=self.request.user)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    template_name = "submits/detail.html"
    context_object_name = "submission"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return obj
        if obj.user_id != self.request.user.id:
            raise Http404()
        return obj


class SubmissionDeleteView(LoginRequiredMixin, DeleteView):
    model = Submission
    template_name = "submits/confirm_delete.html"
    success_url = reverse_lazy("submits-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if self.request.user.is_staff or self.request.user.is_superuser:
            return obj
        if obj.user_id != self.request.user.id:
            raise Http404()
        return obj


class SubmissionExportView(LoginRequiredMixin, View):
    def get(self, request, pk):
        submission = Submission.objects.select_related("input_data", "user").get(pk=pk)
        if not (request.user.is_staff or request.user.is_superuser) and submission.user_id != request.user.id:
            raise Http404()

        input_data = submission.input_data
        header = [
            "naklad_szt",
            "objetosc_m3",
            "konstrukcja_kg",
            "sklejka_m3",
            "drewno_m3",
            "plyta_m2",
            "druk_m2",
            "led_mb",
            "tworzywa_m2",
            "koszty_pozostale",
            "rodzaj_tworzywa",
            "rodzaj_displaya",
            "stopien_skomplikowania",
            "cena",
        ]

        price_value = submission.user_price if submission.user_price is not None else submission.predicted_price

        row = [
            input_data.naklad_szt,
            input_data.objetosc_m3,
            input_data.konstrukcja_kg,
            input_data.sklejka_m3,
            input_data.drewno_m3,
            input_data.plyta_m2,
            input_data.druk_m2,
            input_data.led_mb,
            input_data.tworzywa_m2,
            input_data.koszty_pozostale,
            input_data.rodzaj_tworzywa,
            input_data.rodzaj_displaya,
            input_data.stopien_skomplikowania,
            price_value,
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="submission_{submission.pk}.csv"'
        writer = csv.writer(response, delimiter=";")
        writer.writerow(header)
        writer.writerow(row)
        return response


class SubmissionExportAllView(LoginRequiredMixin, View):
    def get(self, request):
        qs = Submission.objects.select_related("input_data", "user").order_by("-created_at")
        if not (request.user.is_staff or request.user.is_superuser):
            qs = qs.filter(user=request.user)

        header = [
            "naklad_szt",
            "objetosc_m3",
            "konstrukcja_kg",
            "sklejka_m3",
            "drewno_m3",
            "plyta_m2",
            "druk_m2",
            "led_mb",
            "tworzywa_m2",
            "koszty_pozostale",
            "rodzaj_tworzywa",
            "rodzaj_displaya",
            "stopien_skomplikowania",
            "cena",
        ]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="submissions.csv"'
        writer = csv.writer(response, delimiter=";")
        writer.writerow(header)

        for submission in qs:
            input_data = submission.input_data
            price_value = submission.user_price if submission.user_price is not None else submission.predicted_price
            writer.writerow(
                [
                    input_data.naklad_szt,
                    input_data.objetosc_m3,
                    input_data.konstrukcja_kg,
                    input_data.sklejka_m3,
                    input_data.drewno_m3,
                    input_data.plyta_m2,
                    input_data.druk_m2,
                    input_data.led_mb,
                    input_data.tworzywa_m2,
                    input_data.koszty_pozostale,
                    input_data.rodzaj_tworzywa,
                    input_data.rodzaj_displaya,
                    input_data.stopien_skomplikowania,
                    price_value,
                ]
            )

        return response
