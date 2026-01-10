from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# słowniki
RODZAJ_TWORZYWA_CHOICES = [
    ('HIPS', 'HIPS'),
    ('PMMA', 'PMMA'),
    ('PET', 'PET'),
    ('PC', 'PC'),
    ('ABS', 'ABS'),
    ('NAKLEJKA', 'NAKLEJKA'),
    ('GUMA', 'GUMA'),
    ('TKANINA', 'TKANINA')
]

RODZAJ_DISPLAYA_CHOICES = [
    ('ekspozytor_tworzywowy', 'Ekspozytor tworzywowy'),
    ('naladowy', 'Display naladowy'),
    ('potykacz', 'Potykacz'),
    ('regal', 'Regał QPD/HPD/PD'),
    ('paleciak', 'Paleciak QPD/HPD/PD'),
    ('owijka', 'Owijka paletowa'),
    ('kaseton', 'Kaseton'),
    ('wyspa', 'Wyspa'),
    ('druciak', 'Druciak'),
    ('pozostale', 'Pozostałe'),  
]

class EstimationInput(models.Model):
    # NUMERIC
    naklad_szt = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Dodatnia liczba całkowita"
    )
    objetosc_m3 = models.FloatField(default=0)
    konstrukcja_kg = models.FloatField(default=0)
    sklejka_m3 = models.FloatField(default=0)
    drewno_m3 = models.FloatField(default=0)
    plyta_m2 = models.FloatField(default=0)
    druk_m2 = models.FloatField(default=0)
    led_mb = models.FloatField(default=0)
    tworzywa_m2 = models.FloatField(default=0)
    koszty_pozostale = models.FloatField(default=0)
    stopien_skomplikowania = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    # CATEGORICAL z choices
    rodzaj_tworzywa = models.CharField(
        max_length=50,
        choices=RODZAJ_TWORZYWA_CHOICES,
        blank=True,
        null=True  # pozwalamy na None jeśli brak tworzywa
    )
    rodzaj_displaya = models.CharField(
        max_length=50,
        choices=RODZAJ_DISPLAYA_CHOICES,
        default='ekspozytor_pmma'
    )

    def clean(self):
        super().clean()
        # Walidacja zależności: jeśli brak tworzywa, nie może być rodzaju tworzywa
        if self.tworzywa_m2 == 0:
            self.rodzaj_tworzywa = None
        # stopien_skomplikowania już waliduje MinValueValidator / MaxValueValidator
        # naklad_szt już waliduje PositiveIntegerField + MinValueValidator

class EstimationResult(models.Model):
    input_data = models.ForeignKey(EstimationInput, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    user_price = models.FloatField(null=False, blank=False, default=0) # wymagane
    created_at = models.DateTimeField(auto_now_add=True)
