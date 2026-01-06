from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .form import EstimationForm
from .models import EstimationInput
from ml.predict import predict_price
from django.views.generic import TemplateView
from ml.predict import MODEL  # importujemy model z predict.py
class EstimationView(LoginRequiredMixin, FormView):
    template_name = "estimations/form.html"
    form_class = EstimationForm
    success_url = "/estimations/result/"

    def form_valid(self, form):
        input_data = form.save()

        # Wywołanie predykcji
        predicted_result = predict_price({
            "naklad_szt": input_data.naklad_szt,
            "objetosc_m3": input_data.objetosc_m3,
            "konstrukcja_kg": input_data.konstrukcja_kg,
            "sklejka_m3": input_data.sklejka_m3,
            "drewno_m3": input_data.drewno_m3,
            "plyta_m2": input_data.plyta_m2,
            "druk_m2": input_data.druk_m2,
            "led_mb": input_data.led_mb,
            "tworzywa_m2": input_data.tworzywa_m2,
            "koszty_pozostale": input_data.koszty_pozostale,
            "stopien_skomplikowania": input_data.stopien_skomplikowania,
            "rodzaj_tworzywa": input_data.rodzaj_tworzywa,
            "rodzaj_displaya": input_data.rodzaj_displaya,
        })

        user_price = form.cleaned_data.get("user_price")

        # Zapis do sesji tylko liczby dla predykcji
        self.request.session["predicted"] = float(predicted_result["predicted"])
        self.request.session["user_price"] = (
            float(user_price) if user_price not in (None, "", 0) else None
        )

        # Zapisujemy informacje o modelu w sesji
        self.request.session["model_info"] = {
            "name": predicted_result["model_name"],
            "mae": predicted_result["mae"],
            "r2": predicted_result["r2"],
            "type": predicted_result["model_type"],
        }

        return super().form_valid(form)


class EstimationResultView(LoginRequiredMixin, TemplateView):
    template_name = "estimations/result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['predicted'] = self.request.session.get('predicted')
        context['user_price'] = self.request.session.get('user_price')

        # Pobranie danych modelu z sesji
        model_info = self.request.session.get('model_info', {})
        context['model_name'] = model_info.get('name')
        context['model_mae'] = model_info.get('mae')
        context['model_r2'] = model_info.get('r2')
        context['model_type'] = model_info.get('type')

        return context