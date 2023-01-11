from django.urls import path
from .views import ListarCoposView

app_name = "consumo"

urlpatterns = [
    path("copos/", view=ListarCoposView.as_view(), name="listar_copos")
]
