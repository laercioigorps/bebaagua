from django.urls import path
from .views import ListarCoposView, RegistrarConsumoCopoView

app_name = "consumo"

urlpatterns = [
    path("copos/", view=ListarCoposView.as_view(), name="listar_copos"),
    path("copos/consumir/<str:username>/", view=RegistrarConsumoCopoView.as_view(), name="consumir_copo"),
]
