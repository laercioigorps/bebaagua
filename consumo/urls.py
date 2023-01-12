from django.urls import path
from .views import RegistrarConsumoView

app_name = "consumo"

urlpatterns = [
    path("copos/consumir/<str:username>/", view=RegistrarConsumoView.as_view(), name="consumir_copo"),
]
