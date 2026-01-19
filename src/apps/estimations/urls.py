from django.urls import path
from .views import EstimationView, EstimationResultView, GeminiVerifyPriceView

urlpatterns = [
    path('', EstimationView.as_view(), name='estimations'),
    path('result/', EstimationResultView.as_view(), name='estimation-result'),
    path('verify/', GeminiVerifyPriceView.as_view(), name='estimation-verify'),
]
