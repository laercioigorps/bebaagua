from django.urls import path
from .views import (
    RegistrarConsumoView,
    ResumoConsumoView,
    CriarPerfilView,
    ListarPerfisView,
    DetalhePerfilView,
    HistoricoConsumoView,
)

app_name = "consumo"

urlpatterns = [
    path("users/", view=CriarPerfilView.as_view(), name="criar_perfil"),
    path("users/listar/", view=ListarPerfisView.as_view(), name="listar_perfis"),
    path(
        "users/<str:username>/", view=DetalhePerfilView.as_view(), name="detalhe_perfil"
    ),
    path(
        "users/<str:username>/consumir/",
        view=RegistrarConsumoView.as_view(),
        name="consumir",
    ),
    path(
        "users/<str:username>/resumo/", view=ResumoConsumoView.as_view(), name="resumo"
    ),
    path(
        "users/<str:username>/resumo/<str:data>/",
        view=ResumoConsumoView.as_view(),
        name="resumo_data",
    ),
    path(
        "users/<str:username>/historico/",
        view=HistoricoConsumoView.as_view(),
        name="historico_consumo",
    ),
]
