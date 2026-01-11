from django.conf import settings
from django.db import models

from apps.estimations.models import EstimationInput


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_data = models.ForeignKey(EstimationInput, on_delete=models.CASCADE)
    predicted_price = models.FloatField()
    user_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Submission #{self.pk} by {self.user}"
