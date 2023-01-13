from django.urls import path
from .views import RegistrarConsumoView, ResumoConsumoView

app_name = "consumo"

urlpatterns = [
    path("copos/consumir/<str:username>/", view=RegistrarConsumoView.as_view(), name="consumir_copo"),
    path("resumo/<str:username>/", view=ResumoConsumoView.as_view(), name="resumo"),
    path("resumo/<str:username>/<str:data>/", view=ResumoConsumoView.as_view(), name="resumo_data"),
]
