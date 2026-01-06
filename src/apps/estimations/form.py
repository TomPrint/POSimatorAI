from django import forms
from .models import EstimationInput

class EstimationForm(forms.ModelForm):
    user_price = forms.DecimalField(
        required=True,  # wymagane
        label="Twoja wycena",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = EstimationInput
        fields = [
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
            "stopien_skomplikowania",
            "rodzaj_tworzywa",
            "rodzaj_displaya",
        ]

        widgets = {
            "naklad_szt": forms.NumberInput(attrs={"class": "form-control"}),
            "objetosc_m3": forms.NumberInput(attrs={"class": "form-control"}),
            "konstrukcja_kg": forms.NumberInput(attrs={"class": "form-control"}),
            "sklejka_m3": forms.NumberInput(attrs={"class": "form-control"}),
            "drewno_m3": forms.NumberInput(attrs={"class": "form-control"}),
            "plyta_m2": forms.NumberInput(attrs={"class": "form-control"}),
            "druk_m2": forms.NumberInput(attrs={"class": "form-control"}),
            "led_mb": forms.NumberInput(attrs={"class": "form-control"}),
            "tworzywa_m2": forms.NumberInput(attrs={"class": "form-control"}),
            "koszty_pozostale": forms.NumberInput(attrs={"class": "form-control"}),
            "stopien_skomplikowania": forms.NumberInput(attrs={"class": "form-control"}),
            "rodzaj_tworzywa": forms.Select(attrs={"class": "form-control"}),
            "rodzaj_displaya": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_rodzaj_tworzywa(self):
        tworzywa_m2 = self.cleaned_data.get("tworzywa_m2")
        rodzaj = self.cleaned_data.get("rodzaj_tworzywa")
        if tworzywa_m2 == 0:
            return None  # brak tworzywa → brak kategorii
        return rodzaj
